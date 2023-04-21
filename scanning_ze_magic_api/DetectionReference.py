import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os
from os import listdir
from os.path import isfile, join
# Personnal photos
filename_ref_W = 'images/references/white.png'
filename_ref_U = 'images/references/blue.png'
filename_ref_B = 'images/references/black.png'
filename_ref_R = 'images/references/red.png'
filename_ref_G = 'images/references/green.png'

# Photos from the internet
filename_ref_WInternet = 'images/references/W.png'
filename_ref_UInternet = 'images/references/U.png'
filename_ref_BInternet = 'images/references/B.png'
filename_ref_RInternet = 'images/references/R.png'
filename_ref_GInternet = 'images/references/G.png'

# Detection de référence
filename_result = 'images/Results/'

def is_color(img_result_gray, filenameRef):

    #open reference image
    img_ref = cv.imread(filenameRef)
    
    # Change the size of the image for better detection
    img_ref = cv.resize(img_ref, dsize=(math.ceil(30),math.ceil(30)))
    
    #Convert to gray
    img_ref_gray = cv.cvtColor(img_ref,cv.COLOR_BGR2GRAY)

    img_copy = img_result_gray.copy()
    
    # Match the reference with the copied image
    method = cv.TM_CCOEFF_NORMED
    res = cv.matchTemplate(img_copy,img_ref_gray,method)

    # Get the max for each result
    list_probability = []
    for i in res:
        list_probability.append(np.amax(i))

    ##
    # SHOW RESULTS
    ##
    # w,h= img_ref_gray.shape
    # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv.rectangle(imgCopy,top_left, bottom_right, 255, 2)
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Resultat donnée'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(imgCopy,cmap = 'gray')
    # plt.title('Rectangle détecté'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(method)
    # plt.show()
    ##
    # END SHOW RESULTS
    ##

    return max(list_probability)

def what_color(img_result_gray):
    color_probability = {}
    # Two sets of references
    # One found on the internet 
    # The other are picture of me
    # The best values is a mean of both

    # Update the each specific color probability
    color_probability.update({"w" :  (is_color(img_result_gray, filename_ref_W)+is_color(img_result_gray, filename_ref_WInternet))/2})
    color_probability.update({"u" : (is_color(img_result_gray, filename_ref_U)+is_color(img_result_gray, filename_ref_UInternet))/2})
    color_probability.update({"b" : (is_color(img_result_gray, filename_ref_B)+is_color(img_result_gray, filename_ref_BInternet))/2})
    color_probability.update({"r" : (is_color(img_result_gray, filename_ref_R)+is_color(img_result_gray, filename_ref_RInternet))/2})
    color_probability.update({"g" : (is_color(img_result_gray, filename_ref_G)+is_color(img_result_gray, filename_ref_GInternet))/2})
    
    # The threshold to know if the card can be the corresponding color
    threshold = 0.5
    
    list_colors = []
    
    #print("The card correspond to all those colors :")
    # We have the most probable color, and a list of all colors that could correspond (for multiple colors images)
    for key in color_probability:
        if(color_probability[key] > threshold):
            #print("->", key)
            list_colors.append(key)
    
    return {"Most" : max(color_probability, key=color_probability.get), "list_colors" : list_colors}


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
        print(what_color(img_result_gray))

# Function to be called by the main
def test_card(img_result):
    # take only top right corner
    w,h,z= img_result.shape
    img_crop= img_result[0:100, h-250:h]
    #convert to grey
    img_result_gray = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)
    return what_color(img_result_gray)
##
# MAIN
##
if __name__ == "__main__" :        
    test_all_cards()

