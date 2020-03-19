"""
生成每一帧新的图片
"""

from PIL import Image, ImageDraw, ImageFont
import cv2
import os
from tqdm import tqdm


def draw(pic):
    img = cv2.imread('pic/' + pic)  # (H, W, C)
    img = img[:, :, (2, 1, 0)]  # BGR to RGB

    blank = Image.new("RGB", [len(img[0]), len(img)], "white")  # len(img[0]) = W, len(img) = H
    drawObj = ImageDraw.Draw(blank)

    n = 10

    font = ImageFont.truetype('C:/Windows/Fonts/Microsoft YaHei UI/msyhbd.ttc', size=n - 1)

    for i in range(0, len(img), n):
        for j in range(0, len(img[i]), n):
            text = '武汉加油'
            # the integer of a color: R + 256 * G + 256**2 * B
            # color = img[i][j][0] + img[i][j][1] * 256 + img[i][j][2] * 256 * 256
            R, G, B = img[i][j][0], img[i][j][1], img[i][j][2]
            # j/n: the sequence num of the character to be printed
            # [j, i]: the upper left corner of the text
            drawObj.text([j, i], text[int(j / n) % len(text)], font=font, fill=(R, G, B))

    blank.save('new/new_' + pic, 'jpeg')


if __name__ == '__main__':
    filelist = os.listdir('pic')
    for file in tqdm(filelist):
        draw(file)
