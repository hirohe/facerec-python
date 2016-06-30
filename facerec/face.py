#coding=utf-8
import cv2

from configure import config

haar_faces = cv2.CascadeClassifier(config.CLASSIFIER_FILE)

def detectSingleFace(image):
    """ 返回脸部区域的边界(x, y, width, height)
        如果没有检测到人脸则返回None
    """
    faces = haar_faces.detectMultiScale(image, 
            scaleFactor=config.HAAR_SCALE_FACTOR, 
            minNeighbors=config.HAAR_MIN_NEIGHBORS, 
            minSize=config.HAAR_MIN_SIZE, 
            flags=cv2.CASCADE_SCALE_IMAGE)
    #是否检测到人脸
    if len(faces) != 1:
        return None
    return faces[0]

def crop(image, x, y, w, h):
    """
    """
    crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
    midy = y + h/2
    y1 = max(0, midy-crop_height/2)
    y2 = min(image.shape[0]-1, midy+crop_height/2)
    return image[y1:y2, x:x+w]

def resize(image):
    """调整图像大小 92x112 以进行图像训练或人脸检测
    """
    return cv2.resize(image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)

def markFace(image):
    result = detectSingleFace(image)
    if result != None:
        x, y, w, h = result
        print result
        cv2.rectangle(image, (x, y), (x+w, y+h), (255,0,0))
    return image