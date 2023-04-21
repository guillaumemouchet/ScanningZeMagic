import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import os
from pytesseract import Output
from os import listdir
from os.path import isfile, join

filename_result = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
##
# OLD CODE could delete
## 
# def old_version(img_result_gray):
#     img_blur = cv.GaussianBlur(img_result_gray, (3, 3), 0)

#     # Performing OTSU threshold
#     thresh = cv.threshold(img_blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    
#     # Specify structure shape and kernel size.
#     # Kernel size increases or decreases the area
#     # of the rectangle to be detected.
#     # A smaller value like (10, 10) will detect
#     # each word instead of a sentence.
#     rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (18, 18))
    
#     # Applying dilation on the threshold image
#     dilation = cv.dilate(thresh, rect_kernel, iterations = 1)
    
#     # Finding contours
#     contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL,
#                                                     cv.CHAIN_APPROX_NONE)
    
#     # Creating a copy of image
#     im2 = img_result_gray.copy()
    
#     # Looping through the identified contours
#     # Then rectangular part is cropped and passed on
#     # to pytesseract for extracting text from it
#     # Extracted text is then written into the text file
#     for cnt in contours:
#         x, y, w, h = cv.boundingRect(cnt)
        
#         # Drawing a rectangle on copied image
#         cv.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         # Cropping the text block for giving input to OCR
#         cropped = im2[y:y + h, x:x + w]
#         # Open the file in append mode
        
#         # Apply OCR on the cropped image
#         text = pytesseract.image_to_string(cropped) #Choose language
        
#         #print(text)
#     # cv.imshow("im2", im2)
#     # cv.waitKey(0)
##
# End of OLD CODE
##

def what_text(img_result_gray):
    all_text = ""
    img_blur = cv.GaussianBlur(img_result_gray, (3, 3), 0)
    
    # Get the data of the image with Tesseract
    # We use a dict to see if tesseract is confident in his answer
    results = pytesseract.image_to_data(img_blur, output_type=Output.DICT)
    
    # for each text in the
    for i in range(0, len(results["text"])):       
        # Get text and confidance in the result
        text = results["text"][i]
        conf = float(results["conf"][i])
        
        # Filter out week confidance and empty text
        if conf > 85 and not(text.isspace()) :
            # add all valid text together
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

        # take only top left corner
        img_crop = img_result[0:100, 0:500]

        #convert to grey
        img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        print(what_text(img_result_gray))

# Function to be called by the main
def test_card(img_result):
    # take only top left corner
    img_crop = img_result[0:100, 0:400]
    #convert to grey
    img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)
    return what_text(img_result_gray)
    
##
# MAIN
##
if __name__ == "__main__" :        
    test_all_cards()
