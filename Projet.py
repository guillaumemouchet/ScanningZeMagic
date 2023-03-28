import cv2 as cv
import numpy as np 
from matplotlib import pyplot as plt
import math
    
filename = 'images/multiple_image.jpg' 

filename = 'images/mtg_cards_4.jpeg' 
filename = 'images/mtg_phone.jpg' 

# convert to the original size for the border
def round_ratio(x):
  return round(x*ratio_y)


# 720x1080 best resolution for the corner detection
img_width= 720
img_heigth= 1080

img = cv.imread(filename)
print(img.shape)
img_copy = img
#Changing the size of the image, while keeping the ratio
ratio_y = 1
if(img.shape[1]>img_width):
    ratio_y = img.shape[1]/img_width
    img_copy = cv.resize(img_copy, dsize=(math.ceil(img.shape[1]/ratio_y),math.ceil(img.shape[0]/ratio_y)))
    
cv.imshow("resized",img_copy)
cv.waitKey(0)

#Normalize the image copied
print(img_copy.shape)
img_normalized = np.zeros((800, 800))
img_normalized = cv.normalize(img_copy,  img_normalized, 0, 255, cv.NORM_MINMAX)
# convert to gray
img_grey = cv.cvtColor(img_normalized,cv.COLOR_BGR2GRAY)
#threshold
#threshold,img_threshold= cv.threshold(img_grey,55,255,cv.THRESH_BINARY)
# apply Gaussian blur to reduce noise
img_blur = cv.GaussianBlur(img_grey, (5, 5), 0)

# detect edges using Canny algorithm
img_edges = cv.Canny(img_blur, 50, 150, apertureSize=3)
#find contours
contours, hierarchy = cv.findContours(img_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# 63 × 88 mm a magic card size

#################3 Not needed since the images are resized ###############################
#min_area = 18000
#max_area = min_area + 12000
# 48000-60000 best for multiple_image.jpg => 1280x720 pixels => 37.5
# TODO-TODO best for all cards => 720xXXX =>                
# 8000-20000 best for mtg_cards_4.jpeg => 474x754 pixels => 16.8
# The conclusion is the best spacing between cards is 12'000
# but depends on the cards size in the first place
# Can a pre-traitement can be done to determine the best spacing for a specific image

#contours = [cnt for cnt in contours if cv.contourArea(cnt) > min_area and cv.contourArea(cnt) < max_area] 
# custom function


list_image = []
for contour in contours:
    approx = cv.approxPolyDP(contour,  0.1 * cv.arcLength(contour, True), True)
    # Detect if we have 4 borders
    if len(approx) == 4 and cv.isContourConvex(approx): 
                 
        #convert approx to the normal image to keep resolution
        round_ratio_v = np.vectorize(round_ratio)
        approx = round_ratio_v(approx)
        
        # Draw contour on original image
        cv.drawContours(img, [approx], 0, (0, 0, 255), 2)

        # Crop card region from image
        x, y, w, h = cv.boundingRect(approx)
        card = img[y:y+h, x:x+w]
        
        
        #unwrap the found images
        rect = cv.minAreaRect(approx)        
        corners = cv.boxPoints(rect).astype(np.float32)

        #Detect the rotation of the image, a while can be done instead of an if
        error_value = 10
        print("-------------------------------------")
        print(corners)
        # delta_a = abs(corners[0][0]-corners[3][0])
        # delta_c = abs(corners[1][0]-corners[2][0])
        # delta_b = abs(corners[0][1]-corners[1][1])
        # delta_d = abs(corners[2][1]-corners[3][1])
        delta_y_1_2 = math.pow(abs(corners[0][1]-corners[1][1]),2)+math.pow(abs(corners[0][0]-corners[1][0]),2)
        delta_y_2_3= math.pow(abs(corners[1][1]-corners[2][1]),2)+math.pow(abs(corners[1][0]-corners[2][0]),2)
        print(rect[-1])
        
        if(delta_y_1_2 > delta_y_2_3): # if we are bigger than the error, we need to rotate the corners to put them in the right order
            print("IN a")
            corners = np.array([corners[1],corners[2],corners[3],corners[0]])
        print(corners)

        #  if(delta_a >= error_value): # if we are bigger than the error, we need to rotate the corners to put them in the right order
        #     print("IN a")
        #     corners = np.array([corners[1],corners[2],corners[3],corners[0]])
        # # Il faut que le premier corner soit celui en bas à gauche de l'image
        
        # Marche pour les images qui sont droites, ne fonctionne pas pour les images penchées
        # GOOD IMAGE CORNERS
        # corners [[a. b.]
        #         [c.  b.]
        #         [c. d.]
        #         [ a. d.]]
        # WRONG IMAGE CORNERS
        # corners [[a  d]
        #         [a   b]
        #         [c   b]
        #         [c.  d]
        
        # IMAGE PENCHEE
        # GOOD IMAGE CORNERS
        # corners [[a  b ]
                #  [a   c]
                #  [d   c ]
                #  [d  b      ]]
        # WRONG IMAGE CORNERS
        # corners [[a. b]
        #  [d  b]
        #  [d   c]
        #  [a   c]]

        
        
        # unwrap the image with a set destination corners
        dest_corners = np.array([[0, 0], [500, 0], [500, 750], [0, 750]], dtype=np.float32)
        M = cv.getPerspectiveTransform(corners, dest_corners)
        unwrapped = cv.warpPerspective(img, M, (500, 750))

        
        # Another way to rotate the image but the proportion are kept and the image is wide
        # angle = rect[-1]
        # if angle < 90:
        #     unwrapped = cv.rotate(unwrapped, cv.ROTATE_90_COUNTERCLOCKWISE) 
        list_image.append(unwrapped)
        
# Custom window
cv.namedWindow("original", cv.WINDOW_NORMAL)
cv.imshow("original",img)
cv.waitKey(0) 

for img in list_image:
    cv.imshow('unwrapped', img)
    cv.waitKey(0) 

cv.waitKey(0) 
cv.destroyAllWindows()