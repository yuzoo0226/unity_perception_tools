# %% import
import collections as cl
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import measure
from skimage.segmentation import clear_border
from skimage.filters import threshold_otsu
from shapely.geometry import Polygon, MultiPolygon
from PIL import Image
import json
import cv2
import glob
import sys
import os

# %% def mask2grayscale
def mask2grayscale(mask_path, save_base_path, max=10, single=False):
    print("===== make mask2grayscale start =====")
    if (single): # １枚のみでテストしたいとき
        mask_image_path = "/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/annotations/maskimg_orig/data_000540.png"
        save_image_path = "/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/annotations/maskimg_grayscale/data_000540.png"
        mask_image_gray = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
        # mask_image_gray_01 = np.where(mask_image_gray == 255, 200, 0) #テスト用
        mask_image_gray_01 = np.where(mask_image_gray == 255, 1, 0)
        print(save_image_path)
        cv2.imwrite(save_image_path, mask_image_gray_01)
        return 0

    for image_num in range(2, max+1):
        mask_image_path = mask_path + "segmentation_" + str(image_num) + ".png"
        save_image_path = save_base_path + "data_" + str(image_num) + ".png"
        mask_image_gray = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
        # mask_image_gray_01 = np.where(mask_image_gray == 255, 200, 0) #テスト用
        mask_image_gray_01 = np.where(mask_image_gray == 255, 1, 0)
        print(save_image_path)
        cv2.imwrite(save_image_path, mask_image_gray_01)

    return 0

# %% proc
if __name__ == '__main__':
    base_path = "/home/yuga/.config/unity3d/DefaultCompany/PerceptionURP/small_map/RGBD_yy6/"
    mask_path = base_path + "SemanticSegmentation_orig/"
    save_base_path = base_path + "Segmentation_grayscale/"
    depth_path = base_path + "Depth/"

    mask2grayscale(mask_path, save_base_path, max=20000)
