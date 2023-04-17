import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import os
from pytesseract import Output
import numbers
import re
# Detection de référence
filenameResult = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def find_match(result):
    pattern = re.compile(r'\d{1,2}/\d{1,2}')
    power, toughness = -1, -1
    for match in re.findall(pattern, "".join(result)):
        print(match)
        
        if match.strip() == '*/*': # * the value is changing
            power, toughness = 0, 0
        elif 'X' in match: # X is defined by the cost
            power, toughness = 0, 0
        else:
            try:
                power, toughness = map(int, match.split('/'))
            except:
                power, toughness = -1, -1
    return power, toughness

def replace_seven(result):
    try:
        if(result[1] == "7"):
            result[1] = "/"
    except Exception :
        print("No index 1 in string")
    return result

def what_text(imgResultGrey):
    gray = cv.medianBlur(imgResultGrey, 3)
    # Get the data of the image with Tesseract
    results = pytesseract.image_to_string(gray, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789/*X", lang="eng")#

    result = replace_seven(list(results))    
    
    power, toughness = find_match(result)

    # Retry one more time but with a gaussianBlur
    if(power ==-1 and toughness ==-1):
        gray = cv.GaussianBlur(imgResultGrey, (3, 3), 0)
        
        # Get the data of the image with Tesseract
        results = pytesseract.image_to_string(gray, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789/*X", lang="eng")#

        result = replace_seven(list(results))    
    
        power, toughness = find_match(result)

    print(f'Power: {power}, Toughness: {toughness}')
    cv.imshow("im2", gray)
    cv.waitKey(0)
    return (power, toughness)

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

        # take only bottom right corner
        img_crop = imgResult[w-120:w, h-150:h]

        #convert to grey
        imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        print(what_text(imgResultGrey))

def test_card(imgResult):
    w,h,z= imgResult.shape

    # take only bottom right corner
    img_crop = imgResult[w-120:w, h-150:h]
    
    #convert to grey
    imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

    return what_text(imgResultGrey)
##
# MAIN
##
if __name__ == "__main__" :
    test_all_cards()
    # img = cv.imread('images/Results/mtg_phone0.png')
    # print(test_card(img))