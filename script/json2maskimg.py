from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import json

# カテゴリが一つしかない前提でのプログラムになっている
# TODO: カテゴリに応じてpolyを分け，色も変えるように改良する

def json2maskimg(json_path, start_image_id=0):
    with open(json_path) as f:
        fj = json.load(f)

    old_image_id = start_image_id # 初期id
    polys = []

    for annotation_id in range (len(fj["annotations"])):
        poly = []
        temp = 0
        current_image_id = fj["annotations"][annotation_id]["image_id"]

        # forで回す数をsegmentationの長さの1/2にする
        # xy分を一回のループで処理するため
        range_num = int(len(fj["annotations"][annotation_id]["segmentation"][0]) / 2)

        for j in range(range_num):
            xy = (fj["annotations"][annotation_id]["segmentation"][0][temp], fj["annotations"][annotation_id]["segmentation"][0][temp+1])
            poly.append(xy)
            temp += 2

        # 確認用
        # print(len(poly))
        polys.append(poly)

        if old_image_id != current_image_id:
            old_image_id = current_image_id
            # print(fj["images"][old_image_id]["file_name"])
            print("change image")
            del polys[-1]
            annotation_id -= 1
            # print(polys)
            break

    return polys

def drawpolys(polys, width=640, height=480, color_type="RGB"):
    if color_type == "RGB":
        im = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(im)
        for i in range(len(polys)):
            draw.polygon(polys[i], fill=(255, 255, 255), outline=(255, 255, 255))
    else:
        pass
        # im = Image.new('RGB', (width, height), (0, 0, 0))
        # draw = ImageDraw.Draw(im)
        # for i in range(len(polys)):
        #     draw.polygon(polys[i], fill=(255, 255, 255), outline=(255, 255, 255))

    plt.imshow(im)
    plt.show()
    im.save("/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/annotations/maskimg_orig/data_000540.png")


if __name__ == '__main__':
    # base_path = "/home/yuga/.config/unity3d/DefaultCompany/PerceptionURP/tests/ZED_720p/"
    base_path = "/media/yuga/DATA/datasets/inabe_annotation/HD2K_16_38_38/GroundTruth/annotations/"
    path = base_path + "instances_default.json"
    zed_widht = 2208
    zed_height = 1242
    polys = json2maskimg(path, start_image_id=1)
    drawpolys(polys, width=zed_widht, height=zed_height)
    # print(polys)
    # print(len(polys))
