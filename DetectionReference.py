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
filenameRefW = 'images/references/W.png'
filenameRefU = 'images/references/U.png'
filenameRefB = 'images/references/B.png'
filenameRefR = 'images/references/R.png'
filenameRefG = 'images/references/G.png'

# Detection de référence
filenameResult = 'images/Results/'

def isColor(imgResultGrey, filenameRef):

    imgRef = cv.imread(filenameRef)
    #for ratio in range(14,16,1):
    imgRef = cv.resize(imgRef, dsize=(math.ceil(30),math.ceil(30)))
    imgRefGrey = cv.cvtColor(imgRef,cv.COLOR_BGR2GRAY)

    #cv.imshow("ref", imgRef)

    w,h= imgRefGrey.shape
    imgCopy = imgResultGrey.copy()
    method = cv.TM_CCOEFF_NORMED

    res = cv.matchTemplate(imgCopy,imgRefGrey,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    listProbability = []

    for i in res:
        listProbability.append(np.amax(i))

    # top_left = max_loc

    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv.rectangle(imgCopy,top_left, bottom_right, 255, 2)
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Resultat donnée'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(imgCopy,cmap = 'gray')
    # plt.title('Rectangle détecté'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(method)
    # plt.show()

    return max(listProbability)

def whatColor(imgResultGrey):
    colorProbability = {}
    # Two sets of references
    # One found on the internet 
    # The other are picture of me
    # Maybe try with both and keep the best values
    colorProbability.update({"White" : isColor(imgResultGrey, filenameRefW)})
    colorProbability.update({"blUe" : isColor(imgResultGrey, filenameRefU)})
    colorProbability.update({"Black" : isColor(imgResultGrey, filenameRefB)})
    colorProbability.update({"Red" : isColor(imgResultGrey, filenameRefR)})
    colorProbability.update({"Green" : isColor(imgResultGrey, filenameRefG)})
    print(colorProbability)
    threshold = 0.5
    listColors = {}     
    print("The card correspond to all those colors :")
    for key in colorProbability:
        if(colorProbability[key] > threshold):
            print("->", key)
            listColors.update({key : colorProbability[key]})
    print("Most probable color is", max(colorProbability, key=colorProbability.get))


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
        img_crop= imgResult[0:100, h-200:h]
        #convert to grey
        imgResultGrey = cv.cvtColor(img_crop,cv.COLOR_BGR2GRAY)
        whatColor(imgResultGrey)


testAllCards()