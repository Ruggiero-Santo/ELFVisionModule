import cv2
import requests
import os
try:
    import json
except ImportError:
    import simplejson as json

API_HOST = 'https://api-eu.faceplusplus.com/facepp/v3/'

class Facepp_Client(object):

    def __init__(self, api_key=None, api_secret=None):

        api_key = os.getenv('FACEpp_KEY', None) if api_key==None else api_key
        api_secret = os.getenv('FACEpp_SECRET', None) if api_secret==None else api_secret

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

        r = requests.post(url, params = self.url_params, files = {'image_file': data})
        return json.loads(r.text)

    def deleteFaceSet(self, outer_id = None, faceset_token = None ):
        url = API_HOST + 'faceset/delete'
        params = self.url_params

        if outer_id:
            params.update({'outer_id': outer_id})
        elif faceset_token:
            params.update({'faceset_token': faceset_token})
        else:
            raise AttributeError('You must define a unique outer_id or face_token.')

        return json.loads(requests.post(url, params = params).text)

    def createFaceSet(self, display_name = None, outer_id = None, face_tokens = None ):
        url = API_HOST + 'faceset/create'
        params = self.url_params

        if not outer_id or not isinstance(outer_id, str):
            raise AttributeError('You must define a unique outer_id')
        params.update({'outer_id': outer_id})

        if display_name:
            params.update({'display_name': display_name})

        if face_tokens:
            if isinstance(face_tokens, list):
                if len(face_tokens) <= 5:
                    params.update({'face_tokens': ",".join(face_tokens)})
                else:
                    raise AttributeError('face_tokens array must be length at most 5.')
            elif isinstance(face_tokens, str):
                params.update({'face_tokens': face_tokens})
            else:
                raise AttributeError('face_tokens should be a string or a list of string. You provided a ' + type(face_tokens).__name__ + 'instead.')

        print("paramse:----"+ str(params))
        return json.loads(requests.post(url, params = params).text)

    def addFace(self, face_tokens, faceset_token = None, outer_id = None):
        url = API_HOST + "faceset/addface"
        params = self.url_params

        if not faceset_token and not outer_id:
            raise AttributeError('Missing faceset_token or outer_id argument. At least one must be set.')

        if face_tokens:
            if isinstance(face_tokens, list):
                if len(face_tokens) < 5:
                    params.update({'face_tokens': ",".join(face_tokens)})
                else:
                    raise AttributeError('face_tokens array must be length at most 5.')
            elif isinstance(face_tokens, str):
                params.update({'face_tokens': face_tokens})
            else:
                raise AttributeError('face_tokens should be a string or a list of string. You provided a ' + type(face_tokens).__name__ + 'instead.')

        if outer_id:
            params.update({'outer_id': outer_id})
        elif faceset_token:
            params.update({'faceset_token': faceset_token})
        else:
            raise AttributeError('You must define a unique outer_id  or  face_token.')

        return json.loads(requests.post(url, params = params).text)

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
                raise TypeError("Attributes should be a str. You've provided a " + type(attributes).__name__ + ", instead.")
