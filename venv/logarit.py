import cv2 as cv
def Chuyen_doi_logarit(img, c):
    a = float(c) * cv.log(1.0 + img)
    return round(a)