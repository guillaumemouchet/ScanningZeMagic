import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import os
from pytesseract import Output
import numbers
# Detection de référence
filenameResult = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def what_text(imgResultGrey):
    allText = ""
    img_blur = cv.GaussianBlur(imgResultGrey, (3, 3), 0)
    gray = cv.threshold(img_blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    gray = cv.medianBlur(gray, 3)
    gray = cv.morphologyEx(gray, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_RECT, (3,3)))
    gray = cv.dilate(gray, (3,3), iterations=2)
    gray = cv.erode(gray, (3,3), iterations=3)
    gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        # Get the data of the image with Tesseract
    results = pytesseract.image_to_string(gray, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789/*X")
    
    print(results)
    if results.strip() == '*/*': # * the value is changing
        power, toughness = 0, 0
    elif 'X' in results: # X is defined by the cost
        power, toughness = 0, 0
    else:
        try:
            power, toughness = map(int, results.split('/'))
        except:
            power, toughness = "Error", "Error"


    print(f'Power: {power}, Toughness: {toughness}')
    #cv.imshow("im2", imgResultGrey)
    cv.waitKey(0)
    return allText



def test_all_cards():
    name_of_files = []
    directories = os.listdir(filenameResult)
    for file in directories:
        name_of_files.append(file)
     
    for name in name_of_files:
        print("-----------------------------------------------------")
        print("\t\t\t " + name + "\t\t\t")
        print("-----------------------------------------------------")

        imgResult = cv.imread(filenameResult+name)
        w,h,z= imgResult.shape

        # take only top right corner
        img_crop = imgResult[w-150:w, h-250:h]
        #convert to grey
        imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        print(what_text(imgResultGrey))

##
# MAIN
##
test_all_cards()