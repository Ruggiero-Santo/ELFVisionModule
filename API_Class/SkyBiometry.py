from API_Class.SDK.sky_biometry_client import FaceClient

class SkyBiometry():

    def __init__(self):
        self.init = True

    def __init__(self, key, secret):
        self.client = FaceClient(key, secret)
        self.init = False

    def initializer(self):
        if client:
            self.client = FaceClient(SkyBiometry.key, SkyBiometry.secret)

    def caller(self, frame):
        response = self.client.faces_detect(buffer=frame)
        print(response)
        return frame

    def finalizer(self):
        pass
