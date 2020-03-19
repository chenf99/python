"""
合成新的视频
"""

import os
import cv2
import re


def picvideo(path, size):
    filelist = os.listdir(path)
    filelist.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    '''
    fps:
    帧率：1秒钟有n张图片写进去[控制一张图片停留5秒钟，那就是帧率为1，重复播放这张图片5次]
    如果文件夹下有50张 534*300的图片，这里设置1秒钟播放5张，那么这个视频的时长就是10秒
    '''
    fps = 24
    file_path = 'video/new.mp4'  # 导出路径
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）

    video = cv2.VideoWriter(file_path, fourcc, fps, size)

    for item in filelist:
        if item.endswith('.jpg'):  # 判断图片后缀是否是.jpg
            item = path + '/' + item
            img = cv2.imread(item)
            video.write(img)

    video.release()  # 释放


if __name__ == "__main__":
    picvideo(r'new', (960, 544))
