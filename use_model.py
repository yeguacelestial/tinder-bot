import numpy as np
import os
import pandas as pd
import PIL
import urllib

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image

from io import BytesIO

# Define paths
local_path = os.path.abspath(os.getcwd())
if not os.path.isdir(local_path):
    local_path = None

models_path = os.path.relpath('models')

if local_path:
    models_path = os.path.join(local_path, models_path)

# Load trained model
model = load_model(os.path.join(models_path, 'beauty_model_untuned.h5'))

def predict_from_img_path(img_foldername='images', img_filename='scarlett_johansson.jpg'):
    img_size = 224
    img = image.load_img(os.path.join(local_path, img_foldername, img_filename), target_size=(img_size, img_size))

    # Preprocess image
    img = image.img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)[0][0]
    # print(f'\n{img_filename} - PUNTUACION: ', prediction)

    return img_filename, prediction

def predict_from_url_path(URL):
    with urllib.request.urlopen(URL) as url:
        img = image.load_img(BytesIO(url.read()), target_size=(224, 224))

    img = image.img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)[0][0]

    return prediction

predict_from_url_path(URL='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Scarlett_Johansson_by_Gage_Skidmore_2_%28cropped%2C_2%29.jpg/800px-Scarlett_Johansson_by_Gage_Skidmore_2_%28cropped%2C_2%29.jpg')