import cv2
import os
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

def getInfo(file_path):
    info = {}
    filepath, filename = os.path.split(file_path)
    info["name"] = filename
    
    if os.path.exists(file_path):
        info["size"] = os.path.getsize(file_path)
        info["sizeUnit"] = sizeConvert(info["size"])
        
    cap = cv2.VideoCapture(file_path)
    if cap.isOpened():
        # get方法参数按顺序对应下表（从0开始编号)
        rate = cap.get(5)  # 帧速率
        frame_number = cap.get(7)  # 视频文件的帧数
        info["rate"] = rate
        info["duration"] = int(frame_number / rate)
        info["durationHMS"] = timeConvert(info["duration"])
        info["width"]=int(cap.get(3))
        info["height"]=int(cap.get(4))
        cap.release()
    return info
    
def timeConvert(seconds, str = True):
    h = seconds // 3600
    m = seconds % 3600 // 60
    s = seconds % 60
    if str:
        if h > 0:
            return '{:.0f}:{:.0f}:{:.0f}'.format(h, m, s)
        else:
            return '{:.0f}:{:.0f}s'.format(m, s)
    else:
        return h, m, s
        
def sizeConvert(size):# 单位换算
    K, M, G = 1024, 1024**2, 1024**3
    if size >= G:
        return str(size//G)+'GB'
    elif size >= M:
        return str(size//M)+'MB'
    elif size >= K:
        return str(size//K)+'KB'
    else:
        return str(size)+'Bytes'

def getFrames(file_path, img_path, cutTimes = [1]):
    '''
    file_path: 文件名
    cutTimes： 抽取帧的时间数组，时间单位为s
    return [时间, 帧图像]数组
    '''
    t_frames = []
    
    info = getInfo(file_path)
    cutFrames = [int(info["rate"] * x) + 1  for x in cutTimes ] 
    print("cutFrames:", cutFrames)
    cap = cv2.VideoCapture(file_path)
    cut_cnt = 0
    for cutFrame in cutFrames:
        cap.set(cv2.CAP_PROP_POS_FRAMES,cutFrame -1)
        ret, frame = cap.read()
        if ret:
            t_frames.append( (cutTimes[cut_cnt], frame) )
            cut_cnt += 1
            print("截取视频第：" + str(cut_cnt) + " 帧")
        else:
            break
    cap.release()
    frame = t_frames[0][1]
    cv2.imencode('.jpg', frame)[1].tofile(img_path)
