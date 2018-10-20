import requests
import cv2
import os

class Azure():

    FACE_API = {
        'key': os.getenv('AZURE_FACE', None),
        'url': 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect',
        'params': {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'true',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }
    }

    VISION_API = {
        'key': os.getenv('AZURE_VISION', None),
        'url':'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/analyze',
        'params': {
            'visualFeatures': 'Categories,Description,Color'
        }
    }

    def _drawRectFace(image, jsonResult):
        for face in jsonResult:
            # Draw Rectangle
            fr = face["faceRectangle"]
            origin = (fr["left"], fr["top"])
            size = tuple(map(lambda x, y: x+y, origin, (fr['height'], fr['width'])))
            cv2.rectangle(image, origin, size, (0,255,0), 3)
            # Write gender and emotion
            fa = face["faceAttributes"]
            emotion = max([(value, key) for key, value in fa["emotion"].items()])[1]
            cv2.putText(image,"%s,%s"%(fa["gender"], emotion), origin, cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
            # Draw Landmarks
            fl = face["faceLandmarks"]
            for key, pos in fl.items():
                xy = (int(pos["x"]), int(pos["y"]))
                cv2.circle(image, xy, 1, (0,0,255), -1)

            print(face)

        return image

    def __init__(self, API = "face", API_key = None):

        if API == "face":
            API = self.FACE_API
        if API == "vision":
            API = self.VISION_API

        self.url_API = API['url']
        if API['key'] != None:
            self.headers = {'Ocp-Apim-Subscription-Key': API['key']}
        elif API_key != None:
            self.headers = {'Ocp-Apim-Subscription-Key': API_key}
        else:
            raise ValueError("You must set Env with AZURE_FACE or AZURE_VISION (API you are using) or indicate it as parameters")

        self.params = API['params']


    def initializer(self):
        self.headers.update({'Content-Type': 'application/octet-stream'})

    def caller(self, frame):
        data = cv2.imencode('.png', frame)[1].tobytes()

        response = requests.post(self.url_API, params=self.params, headers=self.headers, data=data)
        res = Azure._drawRectFace(frame, response.json())

        return res

    def finalizer(self):
        pass

    # from PIL import Image,  ImageDraw
    # def call_AzureAPI(url_API, key_API, paramsAPI, url_image = None, path_image = None, data_image = None):
    #
    #     headers = {'Ocp-Apim-Subscription-Key': key_API}
    #     response = image = None
    #
    #     if url_image == None and path_image == None and data_image == None:
    #             raise ValueError('You must specify url_image or pth_image.')
    #     else:
    #         if url_image != None:#Call API with image on cloud (url)
    #             image = Image.open(BytesIO(requests.get(url_image).content))
    #             response = requests.post(api_url, params=params, headers=headers, json={'url': url_image})#url_image
    #         else: #Call API with Own image
    #             if data_image != None:
    #                 data = data_image
    #             else:
    #                 data = image = open(path_image, "rb").read()
    #             headers.update({'Content-Type': 'application/octet-stream'})
    #             response = requests.post(api_url, params=params, headers=headers, data=data)
    #
    #     return (image, response.json())
