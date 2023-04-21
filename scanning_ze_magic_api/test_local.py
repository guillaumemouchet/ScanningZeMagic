import io
from flask import Flask, request, jsonify
import os
from PIL import Image
import base64
import cv2 as cv
import numpy as np
import os
from os import listdir
from os.path import isfile, join

import DrawContours
import DetectionReference
import DetectionName
import DetectionPT
import DetectionCardType
import DetectionCMC
filename_result = 'images/'

def processImage(img_result):

    images = DrawContours.get_cards_in_picture(img_result)
    #print("DrawContours finished")

    response = []
    
    for image in images:
        ColorsDict = DetectionReference.test_card(image)
        #print("-->",ColorsDict)
        #print("\tDetectionReference finished")

        name = DetectionName.test_card(image)
        #print("-->",name)
        #print("\tDetectionText finished")
        
        cardType = DetectionCardType.test_card(image)
        #print("-->",cardType)
        #print("\tDetectionCardType finished")
        
        PT = DetectionPT.test_card(image)
        #print("-->",PT)
        #print("\tDetectionPT finished")
        
        CMC = DetectionCMC.test_card(image)
        #print("-->",CMC)
        #print("\tDetectionCMC finished")
        
        # Traitement du CMC dépendament de la couleur
        total = 0
        # if it has a number of color equal to the number of circle the CMC is the number of circles
        if(len(ColorsDict["list_colors"])==CMC[0]):
            total = CMC[0]
        elif(len(ColorsDict["list_colors"])==0):# if it's color less, we need to keep only the value in the circles
            total = CMC[1]
        else:  #if it has more circles than the number of color
            total = CMC[0]-1 + CMC[1]  #you need to add the value in the circle with the number of circles (-1 for the circle with the values in it)

        response.append({
            "name": name,
            "CMC": total,
            "creature_type": cardType,
            "power": PT[0],
            "defense": PT[1],
            "colors": ColorsDict["list_colors"]
        })
        
    print("--------------------------------------------------------")
    print(response)
    print("--------------------------------------------------------")


def test_all_cards():
    name_of_files = []
    # Get all cards in the result file
    files = [f for f in listdir(filename_result) if isfile(join(filename_result, f))]
    for filename in files:
        name_of_files.append(filename)

    for name in name_of_files:
    #name = name_of_files[5]
        print("-----------------------------------------------------")
        print("\t\t\t " + name + "\t\t\t")
        print("-----------------------------------------------------")
        img_result = cv.imread(filename_result+name)

    #convert to grey
        processImage(img_result)
##
# Main
##
if __name__ == "__main__" :        
    test_all_cards()
 