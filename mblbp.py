import numpy as np
import os
from skimage.io import imread_collection
from skimage.color import rgb2gray
from skimage.feature import multiblock_lbp
from skimage.transform import integral_image

def averageMat(img, i, j, height, width):
    height = height + 1
    width = width + 1
    subregion = img[i:height, j:width]
    # print(subregion)
    mean_subregion = np.mean(subregion)
    # print(mean_subregion)
    return mean_subregion

def genAverageMat(filepath, height, width):
    height = height - 1
    width = width - 1
    # img = io.imread(filepath)
    # img = rgb2gray(img) * 256
    img = filepath
    i = 0
    j = 0
    # print(height)
    # print(width)
    result = []
    while i < img.shape[0]:
        eachrow = []
        while j < img.shape[1]:
            temp = averageMat(img, i, j, height + i, width + j)
            eachrow.append(temp)
            j = j + width + 1

        # Batas Kanan Terakhir Ketika Masih tersisa region citra yang belum dirata-rata tetapi ukurannya lebih kecil dari deskriptor MB-LBP
        j = j - width - 1
        tempJ = img.shape[1] - 1
        if (j != tempJ and j < img.shape[1]):
            j = img.shape[1] - 1
            temp = averageMat(img, i, j, height + i, tempJ)
            eachrow.append(temp)
        ###############################################################
            # print(eachrow)
        # Kondisi batas kanan terakhir citra
        # temp = averageMat(img, i, j-width, height + i, img.shape[1])
        # eachrow.append(temp)
        ###################################
        eachrow = np.array(eachrow)
        # if(i == 0):
        # print(eachrow)
        result.append(eachrow)
        i = i + height + 1
        j = 0
    #Batas bawah citra ketika masih tersisa region citra yang belum dirata-rata

    ##############################################################################

    result = np.array(result)
    return result
    ###################################
    # print(result)

def compare(center, other):
    # print('Other '+str(other))
    # print('Center '+str(center))
    diff = other - center
    if (diff < 0):
        return 0
    return 1

def lbpCompare(matriks):
    i = 0
    j = 0
    result = []
    while i + 2 < matriks.shape[0]:
        eachrow = []
        j = 0
        while j + 2 < matriks.shape[1]:
            resultbit = np.ones(8, dtype=int)
            center = matriks[i + 1, j + 1]
            bit1 = compare(center, matriks[i, j])
            bit2 = compare(center, matriks[i, j + 1])
            bit3 = compare(center, matriks[i, j + 2])
            bit4 = compare(center, matriks[i + 1, j + 2])
            bit5 = compare(center, matriks[i + 2, j + 2])
            bit6 = compare(center, matriks[i + 2, j + 1])
            bit7 = compare(center, matriks[i + 2, j])
            bit8 = compare(center, matriks[i + 1, j])
            resultbit[0] = bit1
            resultbit[1] = bit2
            resultbit[2] = bit3
            resultbit[3] = bit4
            resultbit[4] = bit5
            resultbit[5] = bit6
            resultbit[6] = bit7
            resultbit[7] = bit8
            resultdecimal = np.packbits(resultbit, 0)[0]
            eachrow.append(resultdecimal)
            j = j + 3
        #########################################################################################
        j = j - 3
        if (j < matriks.shape[1]):
            resultbit = np.zeros(8, dtype=int)
            center = 0
            if (i + 1 < matriks.shape[0] and j + 1 < matriks.shape[1]):
                center = matriks[i + 1, j + 1]
            bit1 = 0
            if (i < matriks.shape[0] and j < matriks.shape[1]):
                bit1 = compare(center, matriks[i, j])
            bit2 = 0
            if (i < matriks.shape[0] and j + 1 < matriks.shape[1]):
                bit2 = compare(center, matriks[i, j + 1])
            bit3 = 0
            if (i < matriks.shape[0] and j + 2 < matriks.shape[1]):
                bit3 = compare(center, matriks[i, j + 2])
            bit4 = 0
            if (i + 1 < matriks.shape[0] and j + 2 < matriks.shape[1]):
                bit4 = compare(center, matriks[i + 1, j + 2])
            bit5 = 0
            if (i + 2 < matriks.shape[0] and j + 2 < matriks.shape[1]):
                bit5 = compare(center, matriks[i + 2, j + 2])
            bit6 = 0
            if (i < matriks.shape[0] and j + 1 < matriks.shape[1]):
                bit6 = compare(center, matriks[i + 2, j + 1])
            bit7 = 0
            if (i < matriks.shape[0] and j + 1 < matriks.shape[1]):
                bit7 = compare(center, matriks[i + 2, j])
            bit8 = 0
            if (i < matriks.shape[0] and j + 1 < matriks.shape[1]):
                bit8 = compare(center, matriks[i + 1, j])
            resultbit[0] = bit1
            resultbit[1] = bit2
            resultbit[2] = bit3
            resultbit[3] = bit4
            resultbit[4] = bit5
            resultbit[5] = bit6
            resultbit[6] = bit7
            resultbit[7] = bit8
            resultdecimal = np.packbits(resultbit, 0)[0]
            eachrow.append(resultdecimal)
        #########################################################################################
        i = i + 3
        eachrow = np.array(eachrow)
        result.append(eachrow)
    result = np.array(result)
    return result

def draw(result, lbpcode, height, width, i, j, limitI, limitJ):
    binary = '{0:08b}'.format(lbpcode, "b")
    arr_bits = list(binary)
    ilim = i + height
    jlim = j + width

    # Center
    tempI = i
    tempILim = i + height if i + height < limitI else limitI - 1
    tempJ = j
    tempJLim = j + width if j + width < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        result[i + height:i + height + height, j + width:j + width + width] = 0.75
    ###################################################################################

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[0] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    j = jlim
    jlim = j + width

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[1] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    j = jlim
    jlim = j + width

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[2] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    i = ilim
    ilim = i + height

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[3] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    i = ilim
    ilim = i + height

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[4] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    j = jlim - width - width
    jlim = jlim - width

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[5] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    j = jlim - width - width
    jlim = jlim - width

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[6] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    i = ilim - height - height
    ilim = ilim - height

    tempI = i
    tempILim = ilim if ilim < limitI else limitI - 1
    tempJ = j
    tempJLim = jlim if jlim < limitJ else limitJ - 1

    if (tempI < limitI and tempJ < limitJ):
        if (arr_bits[7] == '1'):
            result[tempI:tempILim, tempJ:tempJLim] = 1
        else:
            result[tempI:tempILim, tempJ:tempJLim] = 0.5

    return result

def drawAll(img, mat_lbp, height, width):
    # height = height - 1
    # width = width - 1
    result = np.ones((img.shape[0], img.shape[1]))
    i = 0
    j = 0
    i_lbp = 0
    j_lbp = 0
    while i_lbp < mat_lbp.shape[0]:
        j = 0
        j_lbp = 0
        while j_lbp < mat_lbp.shape[1]:
            result = draw(result, mat_lbp[i_lbp][j_lbp], height, width, i, j, img.shape[0], img.shape[1])
            j = j + (3 * width)
            j_lbp = j_lbp + 1
        i = i + (3 * height)
        i_lbp = i_lbp + 1
    return result * 255

def compareScikit():
    test_img = np.round(np.random.rand(36, 36) * 256)
    int_img = integral_image(test_img)
    matriks = genAverageMat(test_img, 2, 3)
    mat_lbp = lbpCompare(matriks)
    lbp_2 = multiblock_lbp(int_img, 0, 9, 3, 2)

def findAttributeMBLBPFeature(imgpath, ext, bin, height, width, outputname):
    # imgpath = 'PETAdataset/VIPeR/archive/';
    countfile = np.asarray(os.listdir(imgpath)).shape[0]
    imgpath = imgpath + ext
    # imgpath = 'PETAdataset/VIPeR/archive/*.bmp';
    myfeature = np.zeros((countfile, bin))
    # creating a collection with the available images
    print(imgpath)
    col = imread_collection(imgpath, conserve_memory=True)
    i = 0
    print("ouy")
    for img in col:
        gray_img = rgb2gray(img) * 255
        matriks = genAverageMat(gray_img, height, width)
        mat_lbp = lbpCompare(matriks)
        sortfeature = np.sort(mat_lbp.flatten())
        #Agar range pembagiannya bagus
        hist = np.histogram(sortfeature, bins=bin, range=(0, 256))
        myfeature[i, :] = hist[0][:]
        i = i + 1
        print(i)
    np.save(outputname, myfeature)
    np.savetxt(outputname + '.csv', myfeature, delimiter=',', fmt='%d')

def findAllAttributeMBLBPFeature(imgpath, bin, height, width, outputname):
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
        temp = findAttributeMBLBPFeature(imgpath=str(imgpath + data[0]), bin=bin, height=height, width=width,outputname="", ext=data[2])
        if (result == ""):
            result = temp
        else:
            result = np.concatenate((result, temp))
    np.save(outputname, result)
    np.savetxt(outputname + ".csv", result, delimiter=',', fmt='%d')


def imgMblbpFeature(img, bin, height, width):
    matriks = genAverageMat(img, height, width)
    mat_lbp = lbpCompare(matriks)
    sortfeature = np.sort(mat_lbp.flatten())
    hist = np.histogram(sortfeature, bins=bin)
    return hist[0][:]
