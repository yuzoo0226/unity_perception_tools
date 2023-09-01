import cv2
import numpy as np
import os

def normalize(image, min=0, max=255):
    print(np.max(image))


if __name__ == '__main__':
    image_path = "C:/Users/fryuz/Downloads/HD2K_16_38_38/HD2K_16_38_38/all_images/Depth/depth000000.png"
    image = cv2.imread(image_path, 0)
    normalize(image)
