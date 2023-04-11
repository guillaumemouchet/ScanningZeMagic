import io
from flask import Flask, request, jsonify
import os
from PIL import Image
import base64
import cv2 as cv
import numpy as np

import DrawContours
import DetectionReference
import DetectionText
import DetectionPT


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.get('/test')
def get_test():
    return "Success"

#https://stackoverflow.com/questions/67196395/send-and-receive-back-image-by-post-method-in-python-flask
@app.post('/uploadImage')
def processImage():

    file = request.files['file']
    file_data = np.fromstring(file.read(), np.uint8)
    img = cv.imdecode(file_data, cv.IMREAD_COLOR)
    images = DrawContours.get_cards_in_picture(img)
    print("DrawContours finished")

    ColorsDict = DetectionReference.test_card(images[0])
    print("-->",ColorsDict)
    print("DetectionReference finished")

    text = DetectionText.test_card(images[0])
    print("-->",text)
    print("DetectionText finished")
    
    PT = DetectionPT.test_card(images[0])
    print("-->",PT)
    print("DetectionPT finished")
    #cv.imshow("test", images[0])
    #cv.waitKey(0)

    retval, buffer = cv.imencode('.jpg', images[0])
    image_bytes = buffer.tobytes()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    

    print("About to return")
    return jsonify({
            "name": "Chandra Waifu",
            "extension": "Kaladesh",
            "image": encoded_image,
            "creature_type": "Mega waifu material",
            "power": "6",
            "defense": "9",
            "colors": ["r"]
            },    
            {
            "name": "Atraxa lol",
            "extension": "Phyrexia",
            "image": encoded_image,
            "creature_type": "Running out of ideas for a joke",
            "power": "7",
            "defense": "7",
            "colors": ["w", "u", "g", "b"]
            }
          )

