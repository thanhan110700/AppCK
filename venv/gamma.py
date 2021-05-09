import sys
import numpy as np
def adjust_image_gamma(image, gamma):
    image = np.power(image, gamma)
    max_val = np.max(image.ravel())
    image = image / max_val * 255
    image = image.astype(np.uint8)
    return image
def changeGamma(img,value):
    img_new = adjust_image_gamma(img,value)
    return img_new