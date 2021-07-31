# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import random
import numpy as np
import imageio

'''
    统计颜色分布
'''
def do_color_statistics(img):
    w = img.shape[0]
    h = img.shape[1]
    color_d = {}
    for x in range(w):
        for y in range(h):
            color = img[x][y].tobytes()
            color_d[color] = color_d.get(color, 0) + 1
    arr = sorted(color_d.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    return arr

'''
    执行染色动作
    img_data: 输入图片
    color_bytes: 指定颜色
    sz: 染色范围，1~4 代表周围 4/8/12/20 点
'''
def dye_pixels(img_data, color_bytes, sz = 1):
    # 统计所有染色点的坐标
    points = []
    for x in range(img_data.shape[0]):
        for y in range(img_data.shape[1]):
            if img_data[x][y].tobytes().hex() == color_bytes.hex():
                points.append((x, y))
    color = np.frombuffer(color_bytes, dtype=np.uint8)
    w = img_data.shape[0] - 1
    h = img_data.shape[1] - 1
    for (x, y) in points:
        if sz == 1:
            img_data[max(x-1,0)][y] = color
            img_data[x][max(y-1,0)] = color
            img_data[min(x+1,w)][y] = color
            img_data[x][min(y+1,h)] = color
        else:
            pass
    return img_data

def update_pixels(image_data, color_set = None):
    color_arr = do_color_statistics(image_data)
    if color_set != None:
        return dye_pixels(image_data, color_set)
    else:
        color_bytes = b'\xff\xff\xff\xff'
        while color_bytes == b'\xff\xff\xff\xff':
            idx = random.randint(0, min(RANDOM_TOP, len(color_arr)-1))
            color_bytes = color_arr[idx][0]
        return dye_pixels(image_data, color_bytes)

def magnify(img, times=4):
    (w, h, d) = img.shape
    rzimgarr = np.empty([w*times, h*times, d], dtype = img[0][0][0].dtype)
    for x in range(w):
        for y in range(h):
            for xs in range(times):
                for ys in range(times):
                    xx = x*times + xs
                    yy = y*times + ys
                    rzimgarr[xx][yy] = img[x][y]
    return rzimgarr

def random_back(img, img_org):
    (w, h, d) = img.shape
    for x in range(w):
        for y in range(h):
            # 10% 的概率返回颜色
            if random.randint(0, 9) == 0:
                img[x][y] = img_org[x][y]

if __name__ == "__main__":
    RANDOM_TOP = 5
    FRAMES = 100

    image_data = plt.imread("./img-src/dragon.gif")
    image_data_org = image_data.copy()

    color_arr = do_color_statistics(image_data)
    color_set = color_arr[2][0]
    image_list = []
    for i in range(FRAMES):
        image_data = update_pixels(image_data, None)
        image_list.append(magnify(image_data))
        # random_back(image_data, image_data_org)
        print ('\rprocessing: %d/%d' % (i+1, FRAMES), end='')
    imageio.mimwrite('./img-gen/pic.gif', image_list, duration=0.1)
    print("")
