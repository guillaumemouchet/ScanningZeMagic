import io
from flask import Flask, request, jsonify
import os
from PIL import Image
import base64
import cv2 as cv
import numpy as np

import DrawContours
import DetectionReference
import DetectionName
import DetectionPT
import DetectionCardType


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

    response = []
    
    for image in images:
        ColorsDict = DetectionReference.test_card(image)
        print("-->",ColorsDict)
        print("DetectionReference finished")

        name = DetectionName.test_card(image)
        print("-->",name)
        print("DetectionText finished")
        
        cardType = DetectionCardType.test_card(image)
        print("-->",cardType)
        print("DetectionCardType finished")
        
        PT = DetectionPT.test_card(image)
        print("-->",PT)
        print("DetectionPT finished")
        #cv.imshow("test", images[0])
        #cv.waitKey(0)

        retval, buffer = cv.imencode('.jpg', image)
        image_bytes = buffer.tobytes()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        response.append({
            "name": name,
            "extension": "Kaladesh",
            "image": encoded_image,
            "creature_type": cardType,
            "power": PT[0],
            "defense": PT[1],
            "colors": ColorsDict["listColors"]
        })
        
        
    return jsonify(response)
    
    print("About to return")
    # return jsonify({
    #         "name": name,
    #         "extension": "Kaladesh",
    #         "image": encoded_image,
    #         "creature_type": cardType,
    #         "power": PT[0],
    #         "defense": PT[1],
    #         "colors": ColorsDict["listColors"]
    #         },    
    #         {
    #         "name": "Atraxa lol",
    #         "extension": "Phyrexia",
    #         "image": encoded_image,
    #         "creature_type": "Running out of ideas for a joke",
    #         "power": "7",
    #         "defense": "7",
    #         "colors": ["w", "u", "g", "b"]
    #         }
    #       )

