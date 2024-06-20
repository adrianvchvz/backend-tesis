import numpy as np
import os
import tensorflow as tf
from io import BytesIO
from flask import Blueprint, request, jsonify
from PIL import Image

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

#Generar un blueprint para la salida de imágenes.
ws_cnn = Blueprint('ws_cnn', __name__)

ruta = r'C:\Users\Adrian\Desktop\TESIS\backend-tesis\src\rdn\modeloV2.h5'
model = None
class_names = ['no_planos', 'planos']  

def load_model():
    global model
    model = tf.keras.models.load_model(ruta, compile=False)
    print('Modelo cargado')
    return model

model = load_model()

@ws_cnn.route('/predict', methods=['POST'])
def predict():
    
    if model is None:
        return jsonify({'error': 'No se pudo cargar el modelo'}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No se subió ninguna imagen'}), 400
    
    image = request.files['image']
    
    # Leer los datos de la imagen y convertirlos en un objeto Image de Pillow
    image = Image.open(BytesIO(image.read()))
    
    # Redimensionar la imagen si es necesario
    image = np.asarray(image.resize((256, 256)))[..., :3]
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.expand_dims(image, axis=0)
    
    # Realizar la predicción utilizando tu modelo
    predictions = model.predict(image)

    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]
    confidence = predictions[0][predicted_class_index] * 100
    
    # Devolver el resultado como JSON
    return jsonify({'predicted_class': predicted_class, 'confidence': confidence})
