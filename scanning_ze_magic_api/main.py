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
import DetectionCMC


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
    #print("DrawContours finished")

    response = []
    
    for image in images:
        ColorsDict = DetectionReference.test_card(image)
        #print("-->",ColorsDict)
        #print("DetectionReference finished")

        name = DetectionName.test_card(image)
        #print("-->",name)
        #print("DetectionText finished")
        
        cardType = DetectionCardType.test_card(image)
        #print("-->",cardType)
        #print("DetectionCardType finished")
        
        PT = DetectionPT.test_card(image)
        #print("-->",PT)
        #print("DetectionPT finished")
        
        CMC = DetectionCMC.test_card(image)
        #print("-->",PT)
        #print("DetectionCMC finished")
        
        # Traitement du CMC dépendament de la couleur
        total = 0
        # if it has a number of color equal to the number of circle the CMC is the number of circles
        if(len(ColorsDict["list_colors"])==CMC[0]):
            total = CMC[0]
        elif(len(ColorsDict["list_colors"])==0):# if it's color less, we need to keep only the value in the circles
            total = CMC[1]
        else:  #if it has more circles than the number of color
            total = CMC[0]-1 + CMC[1]  #you need to add the value in the circle with the number of circles (-1 for the circle with the values in it)

        print(total)
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
            "colors": ColorsDict["list_colors"]
        })
        
        
    return jsonify(response)
    

