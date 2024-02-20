from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

model = load_model('deepfake_cnn_v1.keras')

import logging

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        valid_extensions = ('.jpg', '.jpeg', '.png')

        if not file.filename.lower().endswith(valid_extensions):
            return {"error": "Invalid file type"}

        threshold = 0.5

        if file.content_type.startswith('image/'):
            contents = await file.read()
            img = Image.open(BytesIO(contents)).convert('RGB')
            
            img = img.resize((256, 256)) 
            img_array = np.array(img)
            img_array = np.expand_dims(img_array, axis=0)  
            
            prediction = model.predict(img_array)
            predicted_value = prediction[0][0]  
            
            result = "deepfake" if predicted_value > threshold else "real"
            return {"result": result}
        else:
            return {"error": "File is not an image"}
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}

