#coding=utf-8
"""Raspberry Pi Face Recognition Treasure Box
Positive Image Capture Script
Copyright 2013 Tony DiCola 

Run this script to capture positive images for training the face recognizer.
"""
import face
from configure import config

import cv2
import os
import sys
import glob

def capture(personName):
    # Set the directory of person
    PERSON_DIR = config.POSITIVE_DIR + '/' + personName
    # TODO get camera object
    camera = None
    # Create the directory for positive training images if it doesn't exist.
    if not os.path.exists(config.POSITIVE_DIR):
        os.mkdir(config.POSITIVE_DIR)
    if not os.path.exists(PERSON_DIR):
        os.mkdir(PERSON_DIR)
    # Find the largest ID of existing positive images.
    # Start new images after this ID value.
    files = sorted(glob.glob(os.path.join(PERSON_DIR,
        config.POSITIVE_FILE_PREFIX + personName + '_' + '[0-9][0-9][0-9].pgm')))
    count = 0
    if len(files) > 0:
        # Grab the count from the last filename.
        # ex: 'positive_012.pgm' >> get 012 trans to int 12
        count = int(files[-1][-7:-4])+1
    
    image = camera.read()
    # Convert image to grayscale.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Get coordinates of single face in captured image.
    result = face.detectSingleFace(image)
    if result is None:
        print 'Could not detect single face!'
        return
    x, y, w, h = result
    # Crop image as close as possible to desired face aspect ratio.
    # Might be smaller if face is near edge of image.
    crop = face.crop(image, x, y, w, h)
    # Save image to file.
    filename = os.path.join(PERSON_DIR, config.POSITIVE_FILE_PREFIX + personName + '_' + '%03d.pgm' % count)
    cv2.imwrite(filename, crop)
    
    