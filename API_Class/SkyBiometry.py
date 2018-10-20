from sky_biometry_client import FaceClient
import os

class SkyBiometry():

    def __init__(self):
        self.key = os.getenv('SKYB_KEY', None)
        self.secret = os.getenv('SKYB_SECRET', None)

        self.client = FaceClient(self.key, self.secret)
        self.init = True

    # def initializer(self):
    #     if self.init:
    #         self.client = FaceClient(SkyBiometry.key, SkyBiometry.secret)

    def caller(self, frame):
        response = self.client.faces_detect(buffer=frame)
        print(response)
        return frame

    def finalizer(self):
        pass
