import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import os
from pytesseract import Output
import numbers
import re
from os import listdir
from os.path import isfile, join
# Detection de référence
filename_result = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# We can find some parasistic values with tesseract
# A bit a regex can help to find the needed values with a /
def find_match(result):
    pattern = re.compile(r'\d{1,2}/\d{1,2}')
    power, toughness = -1, -1
    for match in re.findall(pattern, "".join(result)):        
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

# / can often be mismatch with 7
# We can think that if the second value is a 7 that it could be a / instead
def replace_seven(result):
    try:
        if(result[1] == "7" and result[2] != "/"):
            result[1] = "/"
    except Exception :
        print("No index 1 in string")
    return result

def what_text(img_result_gray):
    # In the first place many actions where made on the image but none where giving a good results
    # After many tests and adaptation medianBlur and GaussianBlur where giving the best results
    # So if the medianBlur does'nt work we try with a GaussianBlur, we could add another if the results are not better
    gray = cv.medianBlur(img_result_gray, 3)
    
    # Get the data of the image with Tesseract
    # The config is what tesseract recommands for number, the whitelist helps to keep only possible values
    results = pytesseract.image_to_string(gray, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789/*X", lang="eng")#

    result = replace_seven(list(results))    
    
    power, toughness = find_match(result)

    # Retry one more time but with a gaussianBlur
    if(power ==-1 and toughness ==-1):
        gray = cv.GaussianBlur(img_result_gray, (3, 3), 0)
        
        # Get the data of the image with Tesseract
        results = pytesseract.image_to_string(gray, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789/*X", lang="eng")#

        result = replace_seven(list(results))    
    
        power, toughness = find_match(result)

    return (power, toughness)

def test_all_cards():
    name_of_files = []
    # Get all cards in the result file
    files = [f for f in listdir(filename_result) if isfile(join(filename_result, f))]
    for filename in files:
        name_of_files.append(filename)

    for name in name_of_files:
        print("-----------------------------------------------------")
        print("\t\t\t " + name + "\t\t\t")
        print("-----------------------------------------------------")

        img_result = cv.imread(filename_result+name)
        w,h,z= img_result.shape

        # take only bottom right corner
        img_crop = img_result[w-120:w, h-150:h]

        #convert to grey
        img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        print(what_text(img_result_gray))
# Function to be called by the main
def test_card(img_result):
    w,h,z= img_result.shape

    # take only bottom right corner
    img_crop = img_result[w-120:w, h-150:h]
    
    #convert to grey
    img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

    return what_text(img_result_gray)
##
# MAIN
##
if __name__ == "__main__" :
    test_all_cards()
