import numpy as np
import cv2 as cv
def changeBrightness(img, value):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    if (value >= 0):
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
    else:
        value = -value
        lim = value
        v[v < lim] = 0
        v[v >= lim] -= value
    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img