import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import os
from pytesseract import Output

# Detection de référence
filenameResult = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def old_version(imgResultGrey):
    img_blur = cv.GaussianBlur(imgResultGrey, (3, 3), 0)

    # Performing OTSU threshold
    thresh = cv.threshold(img_blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    
    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (18, 18))
    
    # Applying dilation on the threshold image
    dilation = cv.dilate(thresh, rect_kernel, iterations = 1)
    
    # Finding contours
    contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL,
                                                    cv.CHAIN_APPROX_NONE)
    
    # Creating a copy of image
    im2 = imgResultGrey.copy()
    
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        
        # Drawing a rectangle on copied image
        cv.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        # Open the file in append mode
        
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped) #Choose language
        
        print(text)
    cv.imshow("im2", im2)
    cv.waitKey(0)


def what_text(imgResultGrey):
    allText = ""
    img_blur = cv.GaussianBlur(imgResultGrey, (3, 3), 0)
    
    # Get the data of the image with Tesseract
    results = pytesseract.image_to_data(img_blur, output_type=Output.DICT)
    
    for i in range(0, len(results["text"])):       
        # Get text and confidance in the result
        text = results["text"][i]
        conf = float(results["conf"][i])
        
        # Filter out week confidance and empty text
        if conf > 85 and not(text.isspace()) :
            allText += text+ " "
            
            # Show the confidence of each text
            print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
            print("")

            text = "".join(text).strip()
            # Write text on the image
            x = results["left"][i]
            y = results["top"][i]
            cv.putText(imgResultGrey,
                        text,
                        (x, y - 10), 
                        cv.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 255), 3)
    cv.imshow("im2", imgResultGrey)
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

        # take only top right corner
        img_crop = imgResult[0:100, 0:400]
        #convert to grey
        imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        print(what_text(imgResultGrey))

def test_card(imgResult):
    # take only top right corner
    img_crop = imgResult[0:100, 0:400]
    #convert to grey
    imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

    return what_text(imgResultGrey)
    
##
# MAIN
##
if __name__ == "__main__" :        
    #test_all_cards()
    img = cv.imread('images/Results/mtg_phone0.png')
    print(test_card(img))