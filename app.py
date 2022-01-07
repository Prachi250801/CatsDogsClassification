import base64
import numpy as np
import io
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ["SM_FRAMEWORK"] = "tf.keras"
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import request
from flask import jsonify
from flask import Flask,render_template

app = Flask(__name__,template_folder='templates')

def get_model():
    global model
    model = load_model('VGG16_cats_and_dogs.h5')
    print(" * Model loaded!")

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image

print("* Loading Keras model...")
get_model()
@app.route("/", methods=["GET"])
def index():
    return render_template('predict.html')


@app.route("/predict", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    #print(message)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()

    response = {
        'prediction': {
            'dog': prediction[0][0],
            'cat': prediction[0][1]
        }
    }
    return jsonify(response)

#port = int(os.environ.get('PORT',8080))
if __name__ == "__main__":
   app.run()