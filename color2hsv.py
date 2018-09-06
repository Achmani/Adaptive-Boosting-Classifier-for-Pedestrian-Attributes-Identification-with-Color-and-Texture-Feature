import numpy as np

def convertpythonic(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    Cmax = max(r, g, b)
    Cmin = min(r, g, b)
    delta = Cmax - Cmin

    hue = 0
    saturation = 0
    value = 0
    # Hue Calculation
    if (delta == 0):
        hue = 0
    elif (Cmax == r):
        hue = 60 * (((g - b) / delta) % 6)
    elif (Cmax == g):
        hue = 60 * (((b - r) / delta) + 2)
    elif (Cmax == b):
        hue = 60 * (((r - g) / delta) + 4)
    hue = round(hue)

    # Saturation
    if (Cmax == 0):
        saturation = 0
    else:
        saturation = round(delta / Cmax * 100, 1)

    # value
    value = round(Cmax * 100, 1)
    result = np.array([hue, saturation, value], dtype=float)
    result = np.asanyarray(result)
    return result

def rgb2hsvpythonic(img):
    r = img[:, :, 0].flatten()
    g = img[:, :, 1].flatten()
    b = img[:, :, 2].flatten()
    vfunc = np.vectorize(convertpythonic, otypes=[np.ndarray])
    hsv = vfunc(r, g, b)
    hsv = np.array(hsv.tolist())
    return hsv