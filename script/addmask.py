import cv2
import numpy as np

# base_base_img_path = "/home/yuga/yuga_ws/mmsegmentation/data/moon_v4/images/test/"
base_mask_img_path = "/home/yuga/Downloads/test_pth_10/result_92000_opacity1/"
base_rgb_img_path = "/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/images/"
# base_rgb_img_path = "/home/yuga/.config/unity3d/DefaultCompany/PerceptionURP/small_map/RGBD_yy2/RGB/"

# num = 6
num_str = "000550"

# base_img_path = base_base_img_path + "data_" + num_str + ".jpg"
mask_img_path = base_mask_img_path + "data_" + num_str + ".jpg"
rgb_img_path = base_rgb_img_path + "data_" + num_str + ".png"

# base_img = cv2.imread(base_img_path, 1)
mask_img = cv2.imread(mask_img_path, 1)
rgb_img = cv2.imread(rgb_img_path, 1)

dst = cv2.addWeighted(rgb_img, 0.5, mask_img, 0.7, 5)

cv2.imwrite("/home/yuga/Downloads/test_pth_10/result_92000/rgb_withmask_" + num_str + ".png", dst)
