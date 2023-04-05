import io
from flask import Flask, request, jsonify
import os
from PIL import Image
import base64



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.get('/test')
def get_test():
    return "Success"

#https://stackoverflow.com/questions/67196395/send-and-receive-back-image-by-post-method-in-python-flask
@app.post('/uploadImage')
def processImage():

    file = request.files['file']
    
    img = Image.open(file.stream)
    img = img.convert('L')   # ie. convert to grayscale
    
    buffer = io.BytesIO()
    img.save(buffer, 'png')
    buffer.seek(0)
    
    data = buffer.read()
    data = base64.b64encode(data).decode()
    
    return jsonify({
            "name": "Chandra Waifu",
            "extension": "Kaladesh",
            "image": data,
            "creature_type": "Mega waifu material",
            "power": "6",
            "defense": "9",
            "colors": ["r"]
            },    
            {
            "name": "Atraxa lol",
            "extension": "Phyrexia",
            "image": data,
            "creature_type": "Running out of ideas for a joke",
            "power": "7",
            "defense": "7",
            "colors": ["w", "u", "g", "b"]
            }
          )
