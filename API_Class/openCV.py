import cv2
import os

class openCV():

    def __init__(self):
        self.face = cv2.CascadeClassifier(cv2.data.haarcascades+'/haarcascade_frontalface_default.xml')

    def caller(self, frame):
        faces = self.face.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return frame

    def setAttr(self, attributes=None):
        pass

    def finalizer(self):
        pass
