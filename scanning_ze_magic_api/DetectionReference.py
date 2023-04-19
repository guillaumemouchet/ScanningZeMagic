import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os
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

    img_ref = cv.imread(filenameRef)
    
    # Change the size of the image for better detection
    img_ref = cv.resize(img_ref, dsize=(math.ceil(30),math.ceil(30)))
    
    
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

    #Return the max probability
    return max(list_probability)

def what_color(img_result_gray):
    color_probability = {}
    # Two sets of references
    # One found on the internet 
    # The other are picture of me
    # Maybe try with both and keep the best values
    
    # # Update the each specific color probability
    # color_probability.update({"White" : is_color(img_result_gray, filename_ref_W)})
    # color_probability.update({"blUe" : is_color(img_result_gray, filename_ref_U)})
    # color_probability.update({"Black" : is_color(img_result_gray, filename_ref_B)})
    # color_probability.update({"Red" : is_color(img_result_gray, filename_ref_R)})
    # color_probability.update({"Green" : is_color(img_result_gray, filename_ref_G)})

 # Update the each specific color probability
    color_probability.update({"w" :  (is_color(img_result_gray, filename_ref_W)+is_color(img_result_gray, filename_ref_WInternet))/2})
    color_probability.update({"u" : (is_color(img_result_gray, filename_ref_U)+is_color(img_result_gray, filename_ref_UInternet))/2})
    color_probability.update({"b" : (is_color(img_result_gray, filename_ref_B)+is_color(img_result_gray, filename_ref_BInternet))/2})
    color_probability.update({"r" : (is_color(img_result_gray, filename_ref_R)+is_color(img_result_gray, filename_ref_RInternet))/2})
    color_probability.update({"g" : (is_color(img_result_gray, filename_ref_G)+is_color(img_result_gray, filename_ref_GInternet))/2})
    threshold = 0.5
    list_colors = []
    dic_Colors = {}  
    
    #Get the colors that could be right (For multiple color cards)
    #print("The card correspond to all those colors :")
    for key in color_probability:
        if(color_probability[key] > threshold):
            #print("->", key)
            list_colors.append(key)
            dic_Colors.update({key : color_probability[key]})
    # Get the most probable color
    #print("Most probable color is", max(color_probability, key=color_probability.get))
    return {"Most" : max(color_probability, key=color_probability.get), "list_colors" : list_colors}


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
        what_color(img_result_gray)

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
    # img = cv.imread('images/Results/mtg_phone0.png')
    # test_card(img)
