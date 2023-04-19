import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os
from pytesseract import Output
import pytesseract


# Detection de référence
filename_result = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def number_of_circles(img_result_gray):
    value = 0
    gray = cv.GaussianBlur(img_result_gray, (5, 5), 0)
    
#    Detect circles using Hough Circle Transform
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=30)

    # Check if circles are detected
    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = circles.round().astype("int")
        
        #print the number of circles detected
        #print("Number of circles detected: ", len(circles[0]))

        # Draw circles on the original image
        for (x, y, r) in circles[0]:
            cv.circle(gray, (x, y), r, (0, 255, 0), 2)          
        corners = np.array([[x+r, y-r], [x-r, y-r],[x-r, y+r],[x+r, y+r]], dtype=np.float32)

        if(len(circles[0])>1):
            dest_corners = np.array([[0, 0], [40, 0], [40, 40], [0, 40]], dtype=np.float32)
            M = cv.getPerspectiveTransform(corners, dest_corners)
            unwrapped = cv.warpPerspective(img_result_gray, M, (40, 40))
            unwrapped = cv.flip(unwrapped,1)
            value = value_in_circles(unwrapped)

        #value += value_in_circles(img_result_gray)
        # cv.destroyAllWindows()
        # Voir avec les references (si nbColors == nbCercle faut pas faire -1)
    return (len(circles[0]),value)
    
def value_in_circles(img_result_gray):
    gray = cv.GaussianBlur(img_result_gray, (3,3), 0)

    #gray = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    #gray = cv.medianBlur(gray, 1)
    # gray = cv.morphologyEx(gray, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_RECT, (2,2)))
    #gray = cv.GaussianBlur(gray, (3,3), 0)
    #gray = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    results = pytesseract.image_to_string(gray, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789*X", lang="eng")#

    results = results.strip()
    return int("0"+results)

def what_cmc(img_result_gray):

    #value = value_in_circles(img_crop)
    number = number_of_circles(img_result_gray)
    return number#+number
    


def test_all_cards():
    name_of_files = []
    # Get all cards in the result file
    directories = os.listdir(filename_result)
    for file in directories:
        name_of_files.append(file)
     
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

