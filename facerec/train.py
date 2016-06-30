# -*- coding: utf-8 -*-
import os
import cv2
import fnmatch
import numpy as np

from configure import config, userManager
import face

def walkFiles(walkDir, match = '*'):
    """Generator function to iterate through all files in a directory recursively
    which match the given filename match parameter.
    """
    for root, dirs, files in os.walk(walkDir):
        for fileName in fnmatch.filter(files, match):
            yield os.path.join(root, fileName)        

def prepareImage(fileName):
    """Read an image as grayscale and resize it to the appropriate size for
    training the face recognition model.
    """
    return face.resize(cv2.imread(fileName, cv2.IMREAD_GRAYSCALE))

def normalize(X, low, high, dtype=None):
    """Normalizes a given array in X to a value between low and high.
    Adapted from python OpenCV face recognition example at:
      https://github.com/Itseez/opencv/blob/2.4/samples/python2/facerec_demo.py
    """
    X = np.asarray(X)
    minX, maxX = np.min(X), np.max(X)
    # normalize to [0...1].
    X = X - float(minX)
    X = X / float((maxX - minX))
    # scale to [low...high].
    X = X * (high-low)
    X = X + low
    if dtype is None:
        return np.asarray(X)
    return np.asarray(X, dtype=dtype)

def trainFace(model):
    
    TRAINING_FILE = os.path.join(config.TRAINING_DIR, config.TRAINING_FILE) 
    faces = []
    labels = []
    
    manager = userManager.UserManager()
    
    persons = os.listdir(config.FACES_DIR)
    for person in persons:
        manager.addUser(person)
        user = manager.getUserByName(person)
        print user
        label = int(user['id'])
        personDir = os.path.join(config.FACES_DIR, person)
        for fileName in walkFiles(personDir, '*.pgm'):
            faces.append(prepareImage(fileName))
            labels.append(label)
        
    # Start training model
    model.train(np.asarray(faces), np.asarray(labels))
    # Save model results
    model.save(TRAINING_FILE)
    

