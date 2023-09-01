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

def offsetdepth(depth_path, save_path, image_name="depth_", start_id=2, max_id=10000, offset=None, blur=None, noise_level=None):
    print("===== make depth2JET start =====")
    # for image_num in range(start_id, max_id+1):
    # image_num_str = str(image_num)

    # image_num_str = image_num_str.zfill(6) # 0埋めしたいとき
    # depth_image_path = depth_path + image_name + image_num_str + ".png"
    # save_image_path = save_base_path + "data_" + image_num_str + ".jpg"
    # print(save_image_path)
    depth_image_gray = cv2.imread(depth_path, cv2.IMREAD_GRAYSCALE)
    height, width = depth_image_gray.shape
    if offset != None:
        if offset > 0:
            max_th = 255 - offset
            depth_image_gray = np.where(depth_image_gray < max_th, (depth_image_gray + offset), 255)
        else:
            min_th = abs(offset)
            depth_image_gray = np.where(depth_image_gray > min_th, (depth_image_gray + offset), 0)
            depth_image_gray = depth_image_gray.astype(np.uint8)
    # depth_image_JET = cv2.applyColorMap(depth_image_gray, cv2.COLORMAP_JET)
    cv2.imwrite(save_path, depth_image_gray)

def depth2JET(depth_path, save_base_path, image_name="depth_", start_id=2, max_id=10000, offset=None, blur=None, noise_level=None):
    print("===== make depth2JET start =====")
    for image_num in range(start_id, max_id+1):
        image_num_str = str(image_num)

        # image_num_str = image_num_str.zfill(6) # 0埋めしたいとき
        depth_image_path = depth_path + image_name + image_num_str + ".png"
        save_image_path = save_base_path + "data_" + image_num_str + ".jpg"
        print(save_image_path)
        depth_image_gray = cv2.imread(depth_image_path, cv2.IMREAD_GRAYSCALE)
        temp_max = depth_image_gray.max()
        # unityの関係でDepthが正常に取れていない場合，そのデータは無視する
        if temp_max == 0:
            continue

        height, width = depth_image_gray.shape

        if blur != None:
            depth_image_gray = cv2.blur(depth_image_gray, blur)

        if noise_level != None:
            noise = np.random.randint(0, noise_level, (height, width))
            depth_image_gray = depth_image_gray - noise

        if offset != None:
            if offset > 0:
                max_th = 255 - offset
                depth_image_gray = np.where(depth_image_gray < max_th, (depth_image_gray + offset), 255)
            else:
                min_th = abs(offset)
                depth_image_gray = np.where(depth_image_gray > min_th, (depth_image_gray + offset), 0)
                depth_image_gray = depth_image_gray.astype(np.uint8)
        depth_image_JET = cv2.applyColorMap(depth_image_gray, cv2.COLORMAP_JET)
        cv2.imwrite(save_image_path, depth_image_JET)
        # cv2.imwrite(save_image_path, depth_image_gray)
        # return


if __name__ == '__main__':
    base_path = "/home/yuga/.config/unity3d/DefaultCompany/PerceptionURP/small_map/RGBD_yy6/"
    # base_path = "/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/"
    depth_path = base_path + "Depth/"
    save_base_path = base_path + "Depth_JET_blur_10/"
    image_name = "rgb_"
    start_id = 2
    max_id = 20000
    offset = -147
    blur = (10, 10)
    noise_level = None
    # blur = None
    # noise_level = None

    # depth_path = "/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/Depth_orig/depth000510.png"
    # save_path = "/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/Depth_offset_120/depth000510.png"
    # offsetdepth(depth_path, save_path, offset=160)

    depth2JET(depth_path, save_base_path, image_name, start_id=start_id, max_id=max_id, offset=offset, blur=blur, noise_level=noise_level)
