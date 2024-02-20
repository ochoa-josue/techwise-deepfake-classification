from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from keras.models import load_model
import numpy as np
from PIL import Image
import io
import os

app = FastAPI()
templates = Jinja2Templates(directory="front-end/templates")

MODEL_FILE_PATH = 'deepfake_cnn_v1.keras'

if not os.path.exists(MODEL_FILE_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_FILE_PATH}' not found")

model = load_model(MODEL_FILE_PATH)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        return JSONResponse(content={"message": "File format not supported"}, status_code=400)

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image)
    is_deepfake = prediction[0][0] > 0.5  # assuming your model outputs a probability

    return templates.TemplateResponse("result.html", {"request": request, "is_deepfake": is_deepfake})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
