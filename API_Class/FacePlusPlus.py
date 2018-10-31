import os
import cv2

class FacePlusPlus():

    def _drawRectFace(image, jsonResult):
        faces = jsonResult["faces"]
        for face in faces:
            print(face["face_rectangle"])
            # {w, x, y, h} = face["face_rectangle"]
        return image

    def __init__(self, FACEpp_Key = None, FACEpp_Secret = None):
        key = os.getenv('FACEpp_KEY', None) if FACEpp_Key==None else FACEpp_Key
        secret = os.getenv('FACEpp_SECRET', None) if FACEpp_Secret==None else FACEpp_Secret

        if key == None or key == None:
            raise ValueError("You must set Env with FACEpp_KEY and FACEpp_SECRET (value of your application) or indicate them as parameters.")
        else:
            self.url_params = { 'api_key': key, 'api_secret': secret }
            self.url = 'https://api-eu.faceplusplus.com/facepp/v3/detect'

    def initializer(self):
        self.url_params.update({"return_attributes": "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus"})


    def caller(self, frame):
        import requests
        _files = {'image_file': cv2.imencode('.jpg', frame)[1]}

        response = requests.post(self.url, params = self.url_params, files = _files)
        frame = FacePlusPlus._drawRectFace(frame, response.text)
        print(response.text)
        return frame

    def finalizer(self):
        pass
