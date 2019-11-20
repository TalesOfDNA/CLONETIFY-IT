import numpy as np
import cv2

def save(file_name, image):
    cv2.imwrite(file_name, image)
    return 