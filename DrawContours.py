import cv2 as cv
import numpy as np 
from matplotlib import pyplot as plt
import math

name = 'blue'
filename = 'images/'+name+'.jpg'
RATIO_Y =1

# 720x1080 best resolution for the corner detection
img_width= 720
img_heigth= 1080
# convert to the original size for the border

def resize_image(img):
    img_copy = img.copy()
    global RATIO_Y
    #Changing the size of the image, while keeping the ratio
    if(img.shape[1]>img_width):
        RATIO_Y = img.shape[1]/img_width
        img_copy = cv.resize(img_copy, dsize=(math.ceil(img.shape[1]/RATIO_Y),math.ceil(img.shape[0]/RATIO_Y)))
        return img_copy
    return img_copy

def round_ratio(x):
    global RATIO_Y
    return round(x*RATIO_Y)

def set_up_image(img):
    
    img_copy = resize_image(img)
        
    cv.imshow("resized",img_copy)
    cv.waitKey(0)

    #Normalize the copied image copied
    img_normalized = np.zeros((800, 800))
    img_normalized = cv.normalize(img_copy,  img_normalized, 0, 255, cv.NORM_MINMAX)
    # convert to gray
    img_grey = cv.cvtColor(img_normalized,cv.COLOR_BGR2GRAY)
    
    ## 
    # A threshold was made but a GaussianBlur seemed better
    ## 
    
    # apply Gaussian blur to reduce noise
    img_blur = cv.GaussianBlur(img_grey, (5, 5), 0)

    # detect edges using Canny algorithm
    img_edges = cv.Canny(img_blur, 50, 150, apertureSize=3)
    return img_edges


def detect_the_contours(img_edges, img):
    #find contours
    contours, hierarchy = cv.findContours(img_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 63 × 88 mm a magic card size

    ##
    # In the first place the contours where filtered depending on a max and min area
    # But it always changed depending on the resolution of the image
    # The solution is that all the copied image are resized to 720x1080
    # But the cut on the is made on the original image
    # The old code is left here but can be removed once explained in the paper
    ##
    ################# Not needed since the images are resized ###############################
    #min_area = 18000
    #max_area = min_area + 12000
    # 48000-60000 best for multiple_image.jpg => 1280x720 pixels => 37.5
    # TODO-TODO best for all cards => 720xXXX =>                
    # 8000-20000 best for mtg_cards_4.jpeg => 474x754 pixels => 16.8
    # The conclusion is the best spacing between cards is 12'000
    # but depends on the cards size in the first place
    # Can a pre-traitement can be done to determine the best spacing for a specific image
    #contours = [cnt for cnt in contours if cv.contourArea(cnt) > min_area and cv.contourArea(cnt) < max_area] 


    # We create approximation of the contour to see if it can correspond to a magic card
    list_image = []
    for contour in contours:
        approx = cv.approxPolyDP(contour,  0.1 * cv.arcLength(contour, True), True)
        # Detect if we have 4 borders
        if len(approx) == 4 and cv.isContourConvex(approx): 
                    
            #convert approx to the normal image to keep good resolution
            round_ratio_v = np.vectorize(round_ratio)
            approx = round_ratio_v(approx)
            
            # Draw contour on original image
            cv.drawContours(img, [approx], 0, (0, 0, 255), 2)

            # Crop card region from image
            x, y, w, h = cv.boundingRect(approx)
            #card = img[y:y+h, x:x+w]
            
            #unwrap the found images
            rect = cv.minAreaRect(approx)        
            corners = cv.boxPoints(rect).astype(np.float32)

            ##
            # In the first place to detect the orientation a comparaison of the corners where made
            # But it wasn't a 100% effective, espacially for tilted cards
            # We can see that the a a's are not in the same place in the 2 images
            # Here are exampled on how where structured the image
                            # Not tilted images
                            # GOOD IMAGE CORNERS
                            # corners [[a. b.]
                            #         [c.  b.]
                            #         [c.  d.]
                            #         [a.  d.]]
                            # WRONG IMAGE CORNERS
                            # corners [[a. d.]
                            #         [a.  b.]
                            #         [c.  b.]
                            #         [c.  d.]]
                            
                            # Tilted images
                            # GOOD IMAGE CORNERS
                            # corners [[a. b.]
                                    #  [a. c.]
                                    #  [d. c.]
                                    #  [d. b.]]
                            # WRONG IMAGE CORNERS
                            # corners [[a. b.]
                                    #  [d. b.]
                                    #  [d. c.]
                                    #  [a. c.]]
            # Here where how the deltas where calculated
            # error_value = 10
            # delta_a = abs(corners[0][0]-corners[3][0])
            # delta_c = abs(corners[1][0]-corners[2][0])
            # delta_b = abs(corners[0][1]-corners[1][1])
            # delta_d = abs(corners[2][1]-corners[3][1])
            #  if(delta_a >= error_value): # if we are bigger than the error, we need to rotate the corners to put them in the right order
            #     corners = np.array([corners[1],corners[2],corners[3],corners[0]])
            # # Il faut que le premier corner soit celui en bas à gauche de l'image
            # Another way to rotate the image but the proportion are not kept and the image become wide
            # angle = rect[-1]
            # if angle < 90:
            #     unwrapped = cv.rotate(unwrapped, cv.ROTATE_90_COUNTERCLOCKWISE) 
            
            # A magic card format is 63 × 88 mm a magic card size
            # The deltas are calculated by comparing X axis and Y axis
            delta_y_1_2 = math.pow(abs(corners[0][1]-corners[1][1]),2)+math.pow(abs(corners[0][0]-corners[1][0]),2)
            delta_y_2_3 = math.pow(abs(corners[1][1]-corners[2][1]),2)+math.pow(abs(corners[1][0]-corners[2][0]),2)
            
            # We compare that the height is bigger than the width or else 
            if(delta_y_1_2 > delta_y_2_3):
                corners = np.array([corners[1],corners[2],corners[3],corners[0]])


            # The size is made on the official magic the gathering card format
            # unwrap the image with a set destination corners
            dest_corners = np.array([[0, 0], [630, 0], [630, 880], [0, 880]], dtype=np.float32)
            M = cv.getPerspectiveTransform(corners, dest_corners)
            unwrapped = cv.warpPerspective(img, M, (630, 880))

            list_image.append(unwrapped)
            
            return list_image
        
def display_and_write(list_image):
     # Display and write on all the found cards in the image
    i = 0
    for img in list_image:
        cv.imshow('unwrapped', img)
        cv.imwrite('images/Results/'+name+str(i)+'.png', img)
        i +=1
        cv.waitKey(0)   
##
# Main
##
        
img = cv.imread(filename)
img_edges = set_up_image(img)
list_image = detect_the_contours(img_edges, img) 
display_and_write(list_image)
 