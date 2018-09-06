import numpy as np
import os
import color2hsv as colorme
from skimage.io import imread_collection


def colorfeatureextractpythonic(hbin=8, sbin=0, vbin=0, img=''):
    feature = 0
    img_hsv = colorme.rgb2hsvpythonic(img)
    if (hbin != 0):
        h = img_hsv[:, 0]  # Hue
        histH = np.histogram(h, bins=hbin, range=(0, 360))
        if (feature == 0):
            feature = histH[0][:]
        else:
            feature = np.append(feature, histH[0][:])
    if (sbin != 0):
        s = img_hsv[:, 1]  # Saturation
        histS = np.asarray(np.histogram(s, bins=sbin))
        if (feature == 0):
            feature = histS[0][:]
        else:
            feature = np.append(feature, histS[0][:])
    if (vbin != 0):
        v = img_hsv[:, 2]  # Value
        histV = np.asarray(np.histogram(v, bins=sbin))
        if (feature == 0):
            feature = histV[0][:]
        else:
            feature = np.append(feature, histV[0][:])
    return feature

def findAttributeColorFeature(imgpath, outputname, h, s, v, ext):
    countfile = np.asarray(os.listdir(imgpath)).shape[0]
    count = h + s + v
    myfeature = np.zeros((countfile, count))
    imgpath = imgpath + ext
    print(imgpath)
    col = imread_collection(imgpath, conserve_memory=True)
    i = 0
    for img in col:
        feature = colorfeatureextractpythonic(hbin=h, sbin=s, vbin=v, img=img)
        myfeature[i, :] = np.asarray(feature)
        print(i)
        i = i + 1
    myfeature = np.asarray(myfeature, dtype=int)
    # print(myfeature)
    if (outputname != ""):
        np.save(outputname, myfeature)
        np.savetxt(outputname + ".csv", myfeature, delimiter=',', fmt='%d')
    return myfeature


def findAllPETAAtributeColorFeature(imgpath, outputname, h, s, v):
    my_data = np.array([["3DPeS/archive/", "3dpescolorfeature", "*.bmp"],
                        ["CAVIAR4REID/archive/", "caviar4reidcolorfeature", "*.jpg"],
                        ["CUHK/archive/", "cuhkcolorfeature", "*.png"],
                        ["GRID/archive/", "gridcolorfeature", "*.jpeg"],
                        ["i-LID/archive/", "i-lidcolorfeature", "*.jpg"],
                        ["MIT/archive/", "mitcolorfeature", "*.jpg"],
                        ["PRID/archive/", "pridcolorfeature", "*.png"],
                        ["SARC3D/archive/", "sarc3dcolorfeature", "*.bmp"],
                        ["TownCentre/archive/", "towncentrecolorfeature", "*.jpg"],
                        ["VIPeR/archive/", "vipercolorfeature", "*.bmp"]])
    result = ""
    for data in my_data:
        temp = findAttributeColorFeature(imgpath=str(imgpath + data[0]), outputname="", h=h, s=s, v=v, ext=data[2])
        if (result == ""):
            print("first")
            result = temp
        else:
            result = np.concatenate((result, temp))
            print("second")
    np.save(outputname, result)
    np.savetxt(outputname + ".csv", result, delimiter=',', fmt='%d')


def findAttributeColorFeatureSingle(hbin, sbin, vbin, filepath):
    feature = colorfeatureextractpythonic(hbin=hbin, sbin=sbin, vbin=vbin, img=filepath)
    return np.asarray(feature, dtype=int)


#findAllPETAAtributeColorFeature("PETAdataset/", "asas", 8, 0, 0)
