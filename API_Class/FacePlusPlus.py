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
            self.url_params = { 'api_key': key, 'api_secret': secret, "return_attributes" : "emotion"}
            self.url = 'https://api-eu.faceplusplus.com/facepp/v3/'

    def setAttr(self, attributes=None):
        """
            set attribute to be returned in the response
            for a complete list of attributes and returned json see: https://console.faceplusplus.com/documents/5679127

            params:
                attributes: list of attributes to return
        """
        if attributes is not None:
            if type(attributes) is str:
                self.url_params.update({"return_attributes": attributes, "return_landmark": 2})
            else:
                raise TypeError("attributes should be a str. You've provided a " + type(attributes).__name__ + ", instead.")
        else:
            #all attributes
            self.url_params.update({"return_attributes": "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus", "return_landmark": 2})


    def simple_demo(self, frame):
        response = self.detect(frame = frame)
        frame = drawRectFace(frame, response)
        print(response)
        return frame

    def detect(self, frame = None, file = None, attributes = None):
        """
            Face detection
            for a complete list of attributes and returned json see: https://console.faceplusplus.com/documents/5679127

            params:
                frame: matrix-like object representing a single frame
                File: file object, file descriptor or filepath of the image
                attributes: list of attributes to return, default = [gender,age,smiling,emotion]

            return:
                json object
        """
        url = self.url + 'detect'

        if attributes is not None:
            self.setAttr(attributes = attributes)
        else:
            self.setAttr(attributes = "gender,age,smiling,emotion")

        if frame is not None:
            data = cv2.imencode('.jpg', frame)[1]

        if file is not None:
            if isinstance(file, str):
                data = open(file, 'rb')
            else:
                data = file

        return json.loads(requests.post(url, params = self.url_params, files = {'image_file': data}).text)


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
