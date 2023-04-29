import cv2 as cv
import numpy as np 
import math

name = 'red'
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

    #Normalize the copied image copied
    img_normalized = np.zeros((800, 800))
    img_normalized = cv.normalize(img_copy,  img_normalized, 0, 255, cv.NORM_MINMAX)
    
    # convert to gray
    img_grey = cv.cvtColor(img_normalized,cv.COLOR_BGR2GRAY)
    
    # apply Gaussian blur to reduce noise
    img_blur = cv.GaussianBlur(img_grey, (5, 5), 0)

    # detect edges using Canny algorithm
    img_edges = cv.Canny(img_blur, 50, 150, apertureSize=3)
    return img_edges


def detect_the_contours(img_edges, img):
    #find contours
    contours, hierarchy = cv.findContours(img_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # We create approximation of the contour to see if it can correspond to a card
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
            
            #unwrap the found images
            rect = cv.minAreaRect(approx)        
            
            corners = cv.boxPoints(rect).astype(np.float32)
            # The deltas are calculated by comparing X axis and Y axis
            
            delta_y_1_2 = math.pow(abs(corners[0][1]-corners[1][1]),2)+math.pow(abs(corners[0][0]-corners[1][0]),2)
            delta_y_2_3 = math.pow(abs(corners[1][1]-corners[2][1]),2)+math.pow(abs(corners[1][0]-corners[2][0]),2)
            
       

            # We compare that the height is bigger than the width or else 
            if(delta_y_1_2 > delta_y_2_3):
                corners = np.array([corners[1],corners[2],corners[3],corners[0]])
            
            
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
        cv.imwrite('images/Results/'+name+str(i)+'.png', img)
        i +=1
        

# Function to be called by the main
# returns list of all cards found in the image
def get_cards_in_picture(img):
    img_edges = set_up_image(img)
    list_image = detect_the_contours(img_edges, img) 
    return list_image
    
##
# Main
##
if __name__ == "__main__" :        
    img = cv.imread(filename)
    img_edges = set_up_image(img)
    list_image = detect_the_contours(img_edges, img) 
    display_and_write(list_image)
 