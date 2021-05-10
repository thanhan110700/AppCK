import numpy as np
import cv2 as cv
def changeHue(img,value):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    if (value >= 0):
        lim = 255 - value
        h[h > lim] = 255
        h[h <= lim] += value
    else:
        value = -value
        lim = value
        h[h < lim] = 0
        h[h >= lim] -= value
    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img