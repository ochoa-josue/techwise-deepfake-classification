from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf
import numpy as np

app = Flask(__name__)

model = tf.keras.models.load_model('deepfake_cnn_v1.keras')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received a request")
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    files = request.files.getlist('image')
    
    if not files:
        return jsonify({'error': 'No selected file'}), 400
    
    predictions = []
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                image = Image.open(file.stream).convert('RGB')
                image = image.resize((256, 256))
                image_array = np.asarray(image) / 255.0
                image_array = np.expand_dims(image_array, axis=0)
                
                print(f"Making prediction for {filename}")
                prediction = model.predict(image_array)
                is_deepfake = bool(prediction[0][0] <= 0.5)
                predictions.append({'filename': filename, 'is_deepfake': is_deepfake})
                
            except Exception as e:
                print(f"An error occurred: {e}")
                predictions.append({'filename': filename, 'error': str(e)})
        else:
            predictions.append({'filename': file.filename, 'error': 'Invalid file format'})
    
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
