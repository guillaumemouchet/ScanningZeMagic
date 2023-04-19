import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import os
from pytesseract import Output

# Detection de référence
filename_result = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def what_text(img_result_gray):
    all_text = ""
    img_blur = cv.GaussianBlur(img_result_gray, (3, 3), 0)
    
    # Get the data of the image with Tesseract
    results = pytesseract.image_to_data(img_blur, output_type=Output.DICT)
    
    for i in range(0, len(results["text"])):       
        # Get text and confidance in the result
        text = results["text"][i]
        conf = float(results["conf"][i])
        
        # Filter out week confidance and empty text
        if conf > 85 and not(text.isspace()) :
            all_text += text+ " "
            
            # Show the confidence of each text
            #print("Confidence: {}".format(conf))
            #print("Text: {}".format(text))
            #print("")

            text = "".join(text).strip()
            # Write text on the image
            x = results["left"][i]
            y = results["top"][i]
            cv.putText(img_result_gray,
                        text,
                        (x, y - 10), 
                        cv.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 255), 3)
    # cv.imshow("im2", img_result_gray)
    # cv.waitKey(0)
    return all_text



def test_all_cards():
    name_of_files = []
    directories = os.listdir(filename_result)
    for file in directories:
        name_of_files.append(file)
     
    for name in name_of_files:
        print("-----------------------------------------------------")
        print("\t\t\t " + name + "\t\t\t")
        print("-----------------------------------------------------")

        img_result = cv.imread(filename_result+name)

        # take only top right corner
        img_crop = img_result[450:550, 0:525]
        #convert to grey
        cv.imshow("test", img_crop)
        cv.waitKey(0)
        img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        print(what_text(img_result_gray))

def test_card(img_result):
    # take only top right corner
    img_crop = img_result[450:550, 0:525]
    #convert to grey
    img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

    return what_text(img_result_gray)
    
##
# MAIN
##
if __name__ == "__main__" :        
    test_all_cards()
