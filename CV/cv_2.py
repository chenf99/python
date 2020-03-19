'''
把视频转成一帧帧的图片
'''

import cv2
vidcap = cv2.VideoCapture('video/video.avi')
count = 0
while True:
    # success: whether reach the end of the video
    # image: a frame of the video
    success, image = vidcap.read()
    if not success:
        break
    cv2.imwrite(f"pic/frame{count}.jpg", image)  # save frame as JPEG file
    if cv2.waitKey(10) == 27:   # if press 'ESC'
        break
    count += 1
