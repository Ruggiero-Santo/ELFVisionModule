from .SDK import FaceClient
import os
import cv2
from urllib.parse import urlencode

class SkyBiometry():

    def __init__(self, SKYB_Key = None, SKYB_Secret = None):
        self.key = os.getenv('SKYB_KEY', None) if SKYB_Key==None else SKYB_Key
        self.secret = os.getenv('SKYB_SECRET', None) if SKYB_Secret==None else SKYB_Secret

        if self.key == None or self.key == None:
            raise ValueError("You must set Env with SKYB_KEY and SKYB_SECRET (value of your application) or indicate them as parameters.")
        self.client = FaceClient(self.key, self.secret)

    def initializer(self):
        pass

    def caller(self, frame):
        data = cv2.imencode('.jpg', frame)[1]

        response = self.client.faces_detect(matrix=data)
        print(response)

        return frame

    def finalizer(self):
        pass
