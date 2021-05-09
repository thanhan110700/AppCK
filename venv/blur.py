import numpy as np
import cv2 as cv
def changeBlur(img, value):
    kernel_size = (value + 1, value + 1)
    kernel = np.array(np.ones(kernel_size, np.float32))
    kernel = kernel / (kernel.size)
    img_new = cv.filter2D(img, -1, kernel)
    return img_new