import face
from PyQt4.QtCore import QThread

class Recognizer(QThread):
    
    faceImage = None
    model = None
    result = None
    label = None
    confidence = None
    
    def __init__(self):
        super(Recognizer, self).__init__()
        
    def run(self):
        if self.faceImage is None:
            # print 'face Image is None'
            return

        self.result = face.detectSingleFace(self.faceImage)
        
        if self.result is None:
            # print 'Could not detect single face!'
            return

        if self.model is None:
            # only return result when model is None
            return
        else:
            # print 'face detected'
            x, y, w, h = self.result
            # crop
            crop = face.resize(face.crop(self.faceImage, x, y, w, h))
            self.label, self.confidence = self.model.predict(crop)
    
    def startRec(self, image, model):
        self.faceImage = image
        self.model = model
        
        self.start()
 