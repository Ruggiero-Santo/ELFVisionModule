from .SDK import FaceClient
import os
import cv2

class SkyBiometry():

    def __init__(self, SKYB_Key = None, SKYB_Secret = None):
        self.key = os.getenv('SKYB_KEY', None) if SKYB_Key==None else SKYB_Key
        self.secret = os.getenv('SKYB_SECRET', None) if SKYB_Secret==None else SKYB_Secret

        if self.key == None or self.key == None:
            raise ValueError("You must set Env with SKYB_KEY and SKYB_SECRET (value of your application) or indicate them as parameters.")
        self.client = FaceClient(self.key, self.secret)

    def setAttr(self, attributes=None):
        pass

    def simple_demo(self, frame):
        data = cv2.imencode('.jpg', frame)[1]

        response = self.client.faces_detect(matrix=data)
        frame = drawRectFace(frame, response)

        return frame

    def finalizer(self):
        pass

def drawRectFace(image, jsonResult):
    def percent2Px(percentage, tot):
        return int((tot*percentage)/ 100)

    faces = jsonResult["photos"][0]["tags"]
    img_h, img_w, _ = image.shape
    size = (img_w, img_h)
    for face in faces:
        # Draw Rectangle
        pos = face["center"]
        center_face = tuple(map(lambda p, t: percent2Px(p, t), (pos["x"], pos["y"]), size))
        size_face = tuple(map(lambda p, t: percent2Px(p, t), (face["width"], face["height"]), size))

        origin_face = tuple(map(lambda x, y: x-y//2, center_face, size_face))
        end_face = tuple(map(lambda x, y: x+y, origin_face, size_face))
        cv2.rectangle(image, origin_face, end_face, (0,255,0), 3)

        # Write gender and emotion
        attributes = face["attributes"]
        emotion = attributes["mood"]["value"]
        gender = attributes["gender"]["value"]
        cv2.putText(image,"%s,%s"%(gender, emotion), origin_face, cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)

    return image
