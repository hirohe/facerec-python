import os
#coding=utf-8
# Threshold for the confidence of a recognized face before it's considered a
# positive match.  Confidence values below this threshold will be considered
# a positive match because the lower the confidence value, or distance, the
# more confident the algorithm is that the face was correctly detected.
# Start with a value of 3000, but you might need to tweak this value down if 
# you're getting too many false positives (incorrectly recognized faces), or up
# if too many false negatives (undetected faces).
POSITIVE_THRESHOLD = 2000.0



# Directories which contain the positive and negative training image data.
POSITIVE_DIR = './training/positive'
NEGATIVE_DIR = './training/negative'

# Value for positive and negative labels passed to face recognition model.
# Can be any integer values, but must be unique from each other.
# You shouldn't have to change these values.
POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2

# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'

# Size (in pixels) to resize images for training and prediction.
# Don't change this unless you also change the size of the training images.
FACE_WIDTH  = 92
FACE_HEIGHT = 112

# base dir
BASE_DIR = os.path.abspath('./')
print BASE_DIR

# Face detection cascade classifier configuration.
# You don't need to modify this unless you know what you're doing.
# See: http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html
HAAR_FACES         = 'haarcascade_frontalface_alt.xml'
HAAR_SCALE_FACTOR  = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE      = (30, 30)

# Filename to use when saving the most recently captured image for debugging.
DEBUG_IMAGE = 'capture.pgm'

# Pin Number of Flash light
FLASH_LIGHT_PIN = 40

#Classifier file
CLASSIFIER_FILE = BASE_DIR + '/facerec/haarcascade_frontalface_alt.xml'

# Faces dir
FACES_DIR = BASE_DIR + '/facerec/faces'

#Training dir
TRAINING_DIR = BASE_DIR + '/facerec/training'

# File to save and load face recognizer model.
TRAINING_FILE = TRAINING_DIR + '/training.xml'

#user csv file
USERS_CVS_FILE = BASE_DIR + '/facerec/training/users.csv'
