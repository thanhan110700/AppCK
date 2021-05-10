import numpy as np
import cv2 as cv
def changeSaturation(img,value):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    if (value >= 0):
        lim = 255 - value
        s[s > lim] = 255
        s[s <= lim] += value
    else:
        value = -value
        lim = value
        s[s < lim] = 0
        s[s >= lim] -= value
    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img