import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os
from pytesseract import Output
import pytesseract
from os import listdir
from os.path import isfile, join

filename_result = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


# The CMC must be analysed depending of differents parameters
# if it's color less and with 1 circle, we need to keep only the value in the circles
# if it has a number of color equal to the number of circle the CMC is the number of circles
# if it has more circles than the number of color
# you need to add the value in the circle with the number of circles (-1 for the circle with the values in it)
# The blue mana symbole is a problem because is too close to a 6 and is almost always detected
def what_cmc(img_result_gray):
    value = 0
    gray = cv.GaussianBlur(img_result_gray, (5, 5), 0)
    
    #Detect circles using Hough Circle Transform
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=30)

    # Check if circles are detected
    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = circles.round().astype("int")
        
        #print("Number of circles detected: ", len(circles[0]))

        # Draw circles on the original image
        for (x, y, r) in circles[0]:
            cv.circle(gray, (x, y), r, (0, 255, 0), 2)          
        
        corners = np.array([[x+r, y-r], [x-r, y-r],[x-r, y+r],[x+r, y+r]], dtype=np.float32)

        #if(len(circles[0])>1):
        # We do the detection of the text on a smaller image where the circle was detected for better precision
        dest_corners = np.array([[0, 0], [40, 0], [40, 40], [0, 40]], dtype=np.float32)
        M = cv.getPerspectiveTransform(corners, dest_corners)
        unwrapped = cv.warpPerspective(img_result_gray, M, (40, 40))
        unwrapped = cv.flip(unwrapped,1)
        value = value_in_circles(unwrapped)

        # return the number of circles detected and the value detected in the circles
    return (len(circles[0]),value)

# Detect the number in the last circle    
def value_in_circles(img_result_gray):
    gray = cv.GaussianBlur(img_result_gray, (3,3), 0)

    ##
    # Many thing where tried but as the PT the GaussianBlur gives the best result
    ##
    #gray = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    #gray = cv.medianBlur(gray, 1)
    # gray = cv.morphologyEx(gray, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_RECT, (2,2)))
    #gray = cv.GaussianBlur(gray, (3,3), 0)
    #gray = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    ##
    # End of old code
    ##
    results = pytesseract.image_to_string(gray, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789*X", lang="eng")#

    results = results.strip()
    return int("0"+results)

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
        # take only top right corner
        w,h,z= img_result.shape
        img_crop= img_result[0:100, h-250:h]
        #convert to grey
        img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)
        print("total",what_cmc(img_result_gray))
        
# Function to be called by the main
def test_card(img_result):
    # take only top right corner
    w,h,z= img_result.shape
    img_crop= img_result[0:100, h-250:h]
    #convert to grey
    img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)
    return what_cmc(img_result_gray)
##
# MAIN
##
if __name__ == "__main__" :        
    test_all_cards()

