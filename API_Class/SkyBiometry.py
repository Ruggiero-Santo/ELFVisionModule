from .SDK import FaceClient
import os
import cv2
from urllib.parse import urlencode

class SkyBiometry():

    def _percent2Px(percentage, tot):
        return int((tot*percentage)/ 100)

    def _drawRectFace(image, jsonResult):
        faces = jsonResult["photos"][0]["tags"]
        img_h, img_w, _ = image.shape
        for face in faces:
            # Draw Rectangle
            pos = face["center"]
            x = SkyBiometry._percent2Px(pos["x"], img_w)
            y = SkyBiometry._percent2Px(pos["y"], img_h)

            w = SkyBiometry._percent2Px(face["width"], img_w)
            h = SkyBiometry._percent2Px(face["height"], img_h)

            origin = (x-w//2, y-h//2)
            size = tuple(map(lambda x, y: x+y, origin, (w, h)))

            cv2.rectangle(image, origin, size, (0,255,0), 3)

            # Write gender and emotion
            attributes = face["attributes"]
            emotion = attributes["mood"]["value"]
            gender = attributes["gender"]["value"]
            cv2.putText(image,"%s,%s"%(gender, emotion), origin, cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)

        return image

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
        frame = SkyBiometry._drawRectFace(frame, response)

        return frame

    def finalizer(self):
        pass
