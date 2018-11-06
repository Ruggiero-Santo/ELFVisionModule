import cv2
import requests
try:
    import json
except ImportError:
    import simplejson as json

API_HOST = 'https://api-eu.faceplusplus.com/facepp/v3/'

class Facepp_Client(object):
    def __init__(self, api_key=None, api_secret=None):

        if not api_key or not api_secret:
            raise AttributeError('Missing api_key or api_secret argument')

        self.api_key = api_key
        self.api_secret = api_secret

        self.url_params = { 'api_key': api_key, 'api_secret': api_secret}


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
        url = API_HOST + 'detect'

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

    def setAttr(self, attributes=None):
        """
            set attribute to be returned in the response
            for a complete list of attributes and returned json see: https://console.faceplusplus.com/documents/5679127

            params:
                attributes: list of attributes to return
        """

        self.url_params.update({"return_attributes": "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus", "return_landmark": 2})

        if attributes is not None:
            if type(attributes) is str:
                if attributes != "all":
                    self.url_params.update({"return_attributes": attributes})
            else:
                raise TypeError("attributes should be a str. You've provided a " + type(attributes).__name__ + ", instead.")
