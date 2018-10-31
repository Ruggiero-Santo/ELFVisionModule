import os
import cv2
import requests
try:
    import json
except ImportError:
    import simplejson as json

"""
Image Requirements
Format : JPG (JPEG), PNG
Size : between 48*48 and 4096*4096 (pixels)
File size : no larger than 2MB
Minimal size of face : the bounding box of a detected face is a square. The minimal side length of a square should be no less than 1/48 of the short side of image, and no less than 48 pixels. For example if the size of image is 4096 * 3200px, the minimal size of face should be 66 * 66px.
"""

class FacePlusPlus():

    def __init__(self, FACEpp_Key = None, FACEpp_Secret = None):
        key = os.getenv('FACEpp_KEY', None) if FACEpp_Key==None else FACEpp_Key
        secret = os.getenv('FACEpp_SECRET', None) if FACEpp_Secret==None else FACEpp_Secret

        if key == None or key == None:
            raise ValueError("You must set Env with FACEpp_KEY and FACEpp_SECRET (value of your application) or indicate them as parameters.")
        else:
            self.url_params = { 'api_key': key, 'api_secret': secret }
            self.url = 'https://api-eu.faceplusplus.com/facepp/v3/detect'

    def initializer(self):
        self.url_params.update({"return_attributes": "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus", "return_landmark": 2})


    def caller(self, frame):
        _files = {'image_file': cv2.imencode('.jpg', frame)[1]}

        response = requests.post(self.url, params = self.url_params, files = _files)
        frame = drawRectFace(frame, json.loads(response.text))
        print(response.text)
        return frame

    def detect(self, frame = None, image = None):
        self.url = 'https://api-eu.faceplusplus.com/facepp/v3/detect'
        self.url_params.update({"return_attributes": "gender,age,smiling,emotion"})

        if frame is not None:
            data = cv2.imencode('.jpg', frame)[1]

        if image is not None:
            data = image

        return json.loads(requests.post(self.url, params = self.url_params, files = {'image_file': data}).text)

    def finalizer(self):
        pass


def drawRectFace(image, jsonResult):
    faces = jsonResult["faces"]
    img_h, img_w, _ = image.shape
    size = (img_w, img_h)
    for face in faces:
        # Draw Rectangle
        w, y, x, h = tuple(map(abs, face["face_rectangle"].values()))
        end_face = tuple(map(lambda x, y: x+y, (x, y), (w, h)))
        cv2.rectangle(image, (x, y), end_face, (0,255,0), 3)

        # Draw Landmarks
        fl = face["landmark"]
        for key, pos in fl.items():
            xy = (int(pos["x"]), int(pos["y"]))
            cv2.circle(image, xy, 1, (0,0,255), -1)

    return image
