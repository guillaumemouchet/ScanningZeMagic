import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
from pytesseract import Output
from os import listdir
from os.path import isfile, join
# Detection de référence
filename_result = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def what_text(img_result_gray):
    all_text = ""
    img_blur = cv.GaussianBlur(img_result_gray, (3, 3), 0) # GaussianBlur gives best results on all that was tested
    
    # Get the data of the image with Tesseract
    results = pytesseract.image_to_data(img_blur, output_type=Output.DICT)
    
    for i in range(0, len(results["text"])):       
        # Get text and confidance in the result
        text = results["text"][i]
        conf = float(results["conf"][i])
        
        # Filter out week confidance and empty text
        if conf > 85 and not(text.isspace()) :
            all_text += text+ " "
            
            ##
            # Display
            ##
            # Show the confidence of each text
            #print("Confidence: {}".format(conf))
            #print("Text: {}".format(text))
            #print("")

            # text = "".join(text).strip()
            # # Write text on the image
            # x = results["left"][i]
            # y = results["top"][i]
            # cv.putText(img_result_gray,
            #             text,
            #             (x, y - 10), 
            #             cv.FONT_HERSHEY_SIMPLEX,
            #             1.2, (0, 255, 255), 3)
    # cv.imshow("im2", img_result_gray)
    # cv.waitKey(0)
    ##
    # END Display
    ##
    return all_text



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

        # take only middle
        img_crop = img_result[450:550, 0:525]
        img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        print(what_text(img_result_gray))

# Function to be called by the main
def test_card(img_result):
    # take only middle
    img_crop = img_result[450:550, 0:525]
    #convert to grey
    img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

    return what_text(img_result_gray)
    
##
# MAIN
##
if __name__ == "__main__" :        
    test_all_cards()
