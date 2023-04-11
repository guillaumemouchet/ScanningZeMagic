import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os
# Personnal photos
filenameRefW = 'images/references/white.png'
filenameRefU = 'images/references/blue.png'
filenameRefB = 'images/references/black.png'
filenameRefR = 'images/references/red.png'
filenameRefG = 'images/references/green.png'

# Photos from the internet
filenameRefWInternet = 'images/references/W.png'
filenameRefUInternet = 'images/references/U.png'
filenameRefBInternet = 'images/references/B.png'
filenameRefRInternet = 'images/references/R.png'
filenameRefGInternet = 'images/references/G.png'

# Detection de référence
filenameResult = 'images/Results/'

def is_color(imgResultGrey, filenameRef):

    imgRef = cv.imread(filenameRef)
    
    # Change the size of the image for better detection
    imgRef = cv.resize(imgRef, dsize=(math.ceil(30),math.ceil(30)))
    
    
    imgRefGrey = cv.cvtColor(imgRef,cv.COLOR_BGR2GRAY)

    imgCopy = imgResultGrey.copy()
    
    # Match the reference with the copied image
    method = cv.TM_CCOEFF_NORMED
    res = cv.matchTemplate(imgCopy,imgRefGrey,method)

    # Get the max for each result
    listProbability = []
    for i in res:
        listProbability.append(np.amax(i))

    ##
    # SHOW RESULTS
    ##
    # w,h= imgRefGrey.shape

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
    return max(listProbability)

def what_color(imgResultGrey):
    colorProbability = {}
    # Two sets of references
    # One found on the internet 
    # The other are picture of me
    # Maybe try with both and keep the best values
    
    # # Update the each specific color probability
    # colorProbability.update({"White" : is_color(imgResultGrey, filenameRefW)})
    # colorProbability.update({"blUe" : is_color(imgResultGrey, filenameRefU)})
    # colorProbability.update({"Black" : is_color(imgResultGrey, filenameRefB)})
    # colorProbability.update({"Red" : is_color(imgResultGrey, filenameRefR)})
    # colorProbability.update({"Green" : is_color(imgResultGrey, filenameRefG)})

 # Update the each specific color probability
    colorProbability.update({"White" :  (is_color(imgResultGrey, filenameRefW)+is_color(imgResultGrey, filenameRefWInternet))/2})
    colorProbability.update({"blUe" : (is_color(imgResultGrey, filenameRefU)+is_color(imgResultGrey, filenameRefUInternet))/2})
    colorProbability.update({"Black" : (is_color(imgResultGrey, filenameRefB)+is_color(imgResultGrey, filenameRefBInternet))/2})
    colorProbability.update({"Red" : (is_color(imgResultGrey, filenameRefR)+is_color(imgResultGrey, filenameRefRInternet))/2})
    colorProbability.update({"Green" : (is_color(imgResultGrey, filenameRefG)+is_color(imgResultGrey, filenameRefGInternet))/2})
    threshold = 0.5
    listColors = {}  
    
    #Get the colors that could be right (For multiple color cards)
    print("The card correspond to all those colors :")
    for key in colorProbability:
        if(colorProbability[key] > threshold):
            print("->", key)
            listColors.update({key : colorProbability[key]})
    # Get the most probable color
    print("Most probable color is", max(colorProbability, key=colorProbability.get))
    return {"Most" : max(colorProbability, key=colorProbability.get), "listColors" : listColors}


def test_all_cards():
    name_of_files = []
    # Get all cards in the result file
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
        img_crop= imgResult[0:100, h-200:h]
        #convert to grey
        imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)
        what_color(imgResultGrey)

def test_card(imgResult):
    # take only top right corner
    w,h,z= imgResult.shape
    img_crop= imgResult[0:100, h-200:h]
    #convert to grey
    imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)
    return what_color(imgResultGrey)
##
# MAIN
##
if __name__ == "__main__" :        
    test_all_cards()
    # img = cv.imread('images/Results/mtg_phone0.png')
    # test_card(img)
