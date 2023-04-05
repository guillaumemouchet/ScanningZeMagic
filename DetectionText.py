import cv2 as cv
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
import os
from pytesseract import Output

# Personnal photos
filenameRefW = 'images/references/white.png'
filenameRefU = 'images/references/blue.png'
filenameRefB = 'images/references/black.png'
filenameRefR = 'images/references/red.png'
filenameRefG = 'images/references/green.png'

# Photos from the internet
filenameRefW = 'images/references/W.png'
filenameRefU = 'images/references/U.png'
filenameRefB = 'images/references/B.png'
filenameRefR = 'images/references/R.png'
filenameRefG = 'images/references/G.png'

# Detection de référence
filenameResult = 'images/Results/'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def whatText(imgResultGrey):
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




def whatText2(imgResultGrey):
    img_blur = cv.GaussianBlur(imgResultGrey, (3, 3), 0)

    results = pytesseract.image_to_data(img_blur, output_type=Output.DICT)
    for i in range(0, len(results["text"])):
        # We can then extract the bounding box coordinates
        # of the text region from  the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]
        
        # We will also extract the OCR text itself along
        # with the confidence of the text localization
        text = results["text"][i]
        conf = int(results["conf"][i])
        
        # filter out weak confidence text localizations
        if conf > 85:
            
            # We will display the confidence and text to
            # our terminal
            print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
            print("")
            
            # We then strip out non-ASCII text so we can
            # draw the text on the image We will be using
            # OpenCV, then draw a bounding box around the
            # text along with the text itself
            text = "".join(text).strip()
            cv.rectangle(imgResultGrey,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255), 2)
            cv.putText(imgResultGrey,
                        text,
                        (x, y - 10), 
                        cv.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 255), 3)
    cv.imshow("im2", imgResultGrey)
    cv.waitKey(0)



def testAllCards():
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
        w,h,z= imgResult.shape
        img_crop= imgResult[0:100, 0:400]
        #convert to grey
        imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)

        whatText2(imgResultGrey)


testAllCards()