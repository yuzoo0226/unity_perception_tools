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
from decimal import Decimal, ROUND_HALF_UP

BASE_PATH = "/home/yuga/.config/unity3d/DefaultCompany/PerceptionURP/HMA_ycb/HMA_v8_train"
OUTPUT_JSON_NAME = "hma_test_07"
IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
USE_INDENT = False
FORMAT = "yolo"

def info():
    tmp = cl.OrderedDict()
    tmp["description"] = "HMA data generate by Unity"
    tmp["unity_info"] = "Random seed = 202210"
    tmp["data_type"] = "valid"
    tmp["url"] = "https://www.brain.kyutech.ac.jp/~tamukoh/"
    tmp["version"] = "7.0"
    tmp["year"] = 2022
    tmp["contributor"] = "Yuga Yano"
    tmp["data_created"] = "2022/10/4"
    tmp["image_size"] = "640 x 480"
    return tmp

def licenses():
    tmp = cl.OrderedDict()
    tmp["id"] = 1
    tmp["url"] = "https://www.brain.kyutech.ac.jp/~tamukoh/"
    tmp["name"] = "Kyutech.Tamlab.yano"
    return tmp

def categories(config="hma"):
    tmps = []
    if config == "moon":
        sup = ["crater"]
        categories = ["crater"]
    elif config == "hma":
        sup = ["ycb"]
        categories = ["cheez-it", "sugar_box", "choco_box", "strawberry_box", "spam", "coffee_can", "tuna_can", "pringles", "mustard", "tomato_can",
                    "banana", "strawberry", "apple", "lemon", "peach", "pear", "orange", "plum", "spray_bottle", "cleanser_bottle",
                    "sponge", "pitcher_base", "pitcher_lid", "plate", "bowl", "fork", "spoon", "spatula", "wine_glass", "mug", "marker", "key",
                    "bolt_and_nut", "clamps", "credit_card", "soccer_ball", "soft_ball", "baseball", "tennis_ball", "racquetball", "golf_ball", "marbles", "cup",
                    "brick", "dice", "rope", "chain", "rubiks", "wood_block", "9-peg", "airplane", "lego", "magazine", "t-shirt",
                    "timer", "boss"
                    ]
    for id, category in enumerate(categories):
        tmp = cl.OrderedDict()
        tmp["id"] = id+1
        tmp["name"] = category
        tmp["supercategory"] = sup[0]
        tmps.append(tmp)
    return tmps

# 指定したbase_pathに対して， [RGB, Semaseg, Dataset]のフォルダを取得
def get_file_list(base_path, keys=["SemanticSegmentation", "RGB", "Dataset"]):
    # 指定されたパスからのフォルダ一覧を取得
    dir_names = os.listdir(base_path)
    files = {}
    # 利用したいフォルダの絶対パスを辞書型変数に取得
    for dir_name in dir_names:
        for key in keys:
            if dir_name.startswith(key):
                files[key] = base_path + "/" + dir_name

    # print(files)
    return files

def open_json(fpath):
    try:
        with open(str(fpath)) as f:
            jh = json.load(f)
    except:
        raise ValueError(f"failed to open {fpath} for read")
    return jh

def get_perception_categories(anno_file, show_info=False, supercategory="rdt"):
    fh = open_json(anno_file)
    anno_list = fh['annotation_definitions']
    spec = anno_list[0]
    spec = spec['spec']

    print(f"\n-->building coco categories:")
    coco_category_block = []
    for id, item in enumerate(spec):
        holding = {}
        holding['id'] = id

        holding['name'] = item['label_name']
        # holding['supercategory'] = supercategory

        # 各セグメンテーションにおけるRGB値をint型で取得する
        # まずはfloat型で取得し，255をかける
        float_b = 255 * float(item["pixel_value"]["b"])
        float_g = 255 * float(item["pixel_value"]["g"])
        float_r = 255 * float(item["pixel_value"]["r"])
        # 四捨五入することで，元のint型の値に戻す
        b = Decimal(str(float_b)).quantize(Decimal("0"), rounding=ROUND_HALF_UP)
        g = Decimal(str(float_g)).quantize(Decimal("0"), rounding=ROUND_HALF_UP)
        r = Decimal(str(float_r)).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

        holding["BGR"] = (int(b), int(g), int(r))
        coco_category_block.append(holding)
        if show_info:
            print(id, item)
            print(holding)

    if show_info:
        print(coco_category_block)

    return coco_category_block


def images(rgb_path, ignore, height, width):
    tmps = []
    files = glob.glob(rgb_path + "/*.png")
    files.sort()

    image_id = 0
    for i, file in enumerate(files):

        if i in ignore:
            pass
        else:
            tmp = cl.OrderedDict()
            tmp["license"] = 1
            tmp["id"] = image_id
            tmp["file_name"] = os.path.basename(file)
            tmp["width"] = width
            tmp["height"] = height
            tmp["date_captured"] = ""
            tmp["coco_url"] = "dummy_words"
            tmp["flickr_url"] = "dummy_words"
            tmps.append(tmp)
            image_id += 1
    return tmps



def create_sub_mask_annotation_con(contour, image_id, category_id, annotation_id, is_crowd, poly, area):

    segmentations = []
    polygons = []

    polygons.append(poly)
    segmentation = np.array(poly.exterior.coords).ravel().tolist()
    segmentations.append(segmentation)

    # Combine the polygons to calculate the bounding box and area
    multi_poly = MultiPolygon(polygons)
    x, y, max_x, max_y = multi_poly.bounds
    width = max_x - x
    height = max_y - y
    bbox = [x, y, width, height]
#     area = multi_poly.area

    annotation = {
        'segmentation': segmentations,
        'iscrowd': is_crowd,
        'image_id': image_id,
        'category_id': category_id,
        'id': annotation_id,
        'bbox': bbox,
        'area': area
    }

    return annotation


def annotations(mask_path, coco_category_block, thresh_areasize, is_segment=True):
    print("===== make annotation start =====")
    # マスク画像をすべて取得
    mask_images = glob.glob(mask_path + "/*.png")
    mask_images.sort()

    # jsonファイルより，カテゴリidとそれに対応する色を取得
    category_ids = {}
    for category_info in coco_category_block:
        category_ids[str(category_info["BGR"])] = category_info["id"]
    is_crowd = 0

    # idの初期化
    annotation_id = 0
    image_id = 0
    rgb_image_id = 0

    # アノテーションデータが存在しない画像をデータセットから除外するため，除外する画像のidをリストで保存する
    ignore = []

    # Create the annotations
    annotations = []
    for mask_image_path in mask_images:
        # print(mask_image_path)
        # 画像の読み込み
        mask_image_color = cv2.imread(mask_image_path)
        mask_image_gray = cv2.imread(mask_image_path, 0)
        base_mask_image_name = os.path.basename(mask_image_path)

        # グレースケール画像を元に領域抽出
        contours = cv2.findContours(mask_image_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 領域が一つもない画像が入力された場合
        if len(contours) == 0:
            print("[warning_1]", base_mask_image_name, "no annotation")
            ignore.append(rgb_image_id)
            rgb_image_id += 1
            continue

        # 領域ごとに，ポリゴンとBboxを算出する
        for contour in contours[0]:
            contour_for_poly = [] # Polygon計算用
            for i in range(len(contour)):
                x, y = contour[i][0]
                contour_for_poly.append([x, y])

            # # 抽出した領域における重心の色を抽出し，カテゴリを判別
            # center_x, center_y = np.average(contour_for_poly, axis=0)
            # center_color = mask_image_color[int(center_y), int(center_x), :]
            # center_color_valid = str((center_color[0], center_color[1], center_color[2]))
            #
            # # カテゴリidを初期化
            # category_id = -1
            # for key, id in category_ids.items():
            #     if key == center_color_valid:
            #         category_id = id + 1
            #         # print(key, id)
            category_id, color = get_category_id(contour_for_poly, mask_image_color, category_ids)

            # すべてのカテゴリの色とマッチングしなかったときは計算しない
            if category_id == -1:
                print("cannot find correct category", center_color_valid)
                continue

            # generate segment data
            if is_segment:
                polygons = []
                # ポリゴンによってエラーが出ることがあるので，try exceptで対応（エラーの原因不明）
                try:
                    poly = Polygon(contour_for_poly)
                    poly = poly.simplify(1.0, preserve_topology=False)
    #                 print(poly)

                    # polygonが計算できた時のみ"annotations"に追加する
                    if poly.is_empty == False:
                        polygons.append(poly)
                        multi_poly = MultiPolygon(polygons)
                        area = multi_poly.area
                        if area < thresh_areasize: # 小さすぎるアノテーションデータは無視する
                            pass
                        else:
                            annotation = create_sub_mask_annotation_con(contour, image_id, category_id, annotation_id, is_crowd, poly, area)
                            annotations.append(annotation)
                            annotation_id += 1
                except Exception as e:
                    # print(e)
                    print("[warning_2]", base_mask_image_name, "skipping the counter")

            # without segment data
            else:
                # is_crowd = 0
                # x_list = []
                # y_list = []
                #
                # for x, y in contour_for_poly:
                #     x_list.append(x)
                #     y_list.append(y)
                #
                # min_x = float(np.min(x_list))
                # max_x = float(np.max(x_list))
                # min_y = float(np.min(y_list))
                # max_y = float(np.max(y_list))
                #
                # width = max_x - min_x
                # height = max_y - min_y
                #
                # area = width * height
                # bbox = [min_x, min_y, width, height]
                bbox, area = get_bbox_and_areasize(contour_for_poly, format="yolact")

                annotation = {
                    'iscrowd': is_crowd,
                    'image_id': image_id,
                    'category_id': category_id,
                    'id': annotation_id,
                    'bbox': bbox,
                    'area': area
                }

                annotations.append(annotation)
                annotation_id += 1

        image_id += 1
        rgb_image_id += 1
        if image_id % 100 == 0:
            print("progress: ", image_id)

    # print(len(mask_images),"個のファイルのうち" ,len(ignore), "個はクレータが存在しないため無視しました")
    print("最終的なデータ数は", len(mask_images)-len(ignore), "です")
    print("===== create annotation complete!! =====")
    # print(annotations)
    return annotations, ignore


def get_category_id(contour_for_poly, mask_image_color, category_ids):
    # 抽出した領域における重心の色を抽出し，カテゴリを判別
    center_x, center_y = np.average(contour_for_poly, axis=0)
    # center_x, center_y = contour_for_poly[0]
    center_color = mask_image_color[int(center_y), int(center_x), :]
    center_color_valid = str((center_color[0], center_color[1], center_color[2]))

    # カテゴリidを初期化
    category_id = -1
    for key, id in category_ids.items():
        if key == center_color_valid:
            category_id = id + 1

    return category_id, center_color_valid


def get_bbox_and_areasize(contour_for_poly, format="yolo"):
    is_crowd = 0
    x_list = []
    y_list = []

    for x, y in contour_for_poly:
        x_list.append(x)
        y_list.append(y)

    min_x = float(np.min(x_list))
    max_x = float(np.max(x_list))
    min_y = float(np.min(y_list))
    max_y = float(np.max(y_list))

    width = max_x - min_x
    height = max_y - min_y
    area = width * height

    if format == "yolact":
        bbox = [min_x, min_y, width, height]

    # yoloフォーマットに合わせてスケーリングを行う
    elif format == "yolo":
        width = width / IMAGE_WIDTH
        center_x = (min_x + max_x) / 2
        center_x = center_x / IMAGE_WIDTH
        height = height / IMAGE_HEIGHT
        center_y = (min_y + max_y) / 2
        center_y = center_y / IMAGE_HEIGHT
        bbox = [center_x, center_y, width, height]

    return bbox, area


def proc(format="coco", is_segment=True, use_indent=False):
    # フォルダパス
    base_path = BASE_PATH
    # データの画像サイズ
    width = IMAGE_WIDTH
    height = IMAGE_HEIGHT

    # Unityから生成されるフォルダ名を取得する
    files = get_file_list(base_path)

    # アノテーションの定義ファイルを読み込む
    # マスク画像の色や名前等
    anno_file = files["Dataset"] + "/annotation_definitions.json"
    coco_category_block = get_perception_categories(anno_file)

    # 無視するアノテーションのエリアサイズ
    # 小さすぎるアノテーションデータはノイズになっているが可能性あるため除外する
    thresh_areasize = 1

    if format == "coco":
        query_list = ["info", "licenses", "annotations", "images", "categories", "segment_info"]
        js = cl.OrderedDict()
        for id, query in enumerate(query_list):
            tmp = ""

            # Info
            if query == "info":
                tmp = info()

            # licenses
            elif query == "licenses":
                tmp = licenses()

            # annotation
            elif query == "annotations":
                tmp, ignore = annotations(files["SemanticSegmentation"], coco_category_block, thresh_areasize, is_segment)

            elif query == "images":
                tmp = images(files["RGB"], ignore, height, width)

            elif query == "categories":
                tmp = categories()

            # save it
            js[query_list[id]] = tmp

        # 書き出すjsonのファイル名
        json_name = base_path + "/" + OUTPUT_JSON_NAME + ".json"
        fw = open(json_name, 'w')

        if use_indent:
            json.dump(js, fw, indent=2)
        else:
            json.dump(js, fw)

        print("complete. output file is ", json_name)

    elif format == "yolo":
        # yolo format : https://qiita.com/yarakigit/items/4d4044bc2740cecba92a
        mask_path = files["SemanticSegmentation"]
        # すべての画像を取り出す
        mask_images = glob.glob(mask_path + "/*.png")
        mask_images.sort()

        # jsonファイルより，カテゴリidとそれに対応する色を取得
        category_ids = {}
        for category_info in coco_category_block:
            category_ids[str(category_info["BGR"])] = category_info["id"]

        for mask_image_path in mask_images:
            output_txt = ""
            # print(mask_image_path)
            # 画像の読み込み
            mask_image_color = cv2.imread(mask_image_path)
            mask_image_gray = cv2.imread(mask_image_path, 0)
            base_mask_image_name = os.path.basename(mask_image_path)

            # グレースケール画像を元に領域抽出
            contours = cv2.findContours(mask_image_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 領域が一つもない画像が入力された場合
            if len(contours) == 0:
                print("[warning_1]", base_mask_image_name, "no annotation")
                ignore.append(rgb_image_id)
                rgb_image_id += 1
                continue

            # 領域ごとに，ポリゴンとBboxを算出する
            # print(len(contours[0]))
            for contour in contours[0]:
                # polygon計算用に整形
                contour_for_poly = [] # Polygon計算用
                for i in range(len(contour)):
                    x, y = contour[i][0]
                    contour_for_poly.append([x, y])

                category_id, color = get_category_id(contour_for_poly, mask_image_color, category_ids)
                if category_id == -1:
                    print("cannot get correct id", color)
                    continue

                bbox, area = get_bbox_and_areasize(contour_for_poly, format=format)
                # yoloフォーマットは0からラベルが始まるため，1減らす
                output_txt += str(category_id-1) + " " + str(bbox[0]) + " " + str(bbox[1]) + " " + str(bbox[2]) + " " + str(bbox[3]) + "\n"

            base_rgb_image_name = base_mask_image_name.replace("segmentation", "rgb")
            txt_file_path = files["RGB"] + "/" + os.path.splitext(base_rgb_image_name)[0] + ".txt"

            f = open(txt_file_path, 'w', encoding='UTF-8')
            f.write(output_txt)
            f.close()

            # print(txt_file_path)
            # print(output_txt)




if __name__ == "__main__":
    use_indent = USE_INDENT
    is_segment = False
    format = FORMAT
    proc(format, is_segment, use_indent)
