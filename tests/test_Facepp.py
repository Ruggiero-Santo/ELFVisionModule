import unittest
import cv2
import os
from API_Class import FacePlusPlus


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = FacePlusPlus()
        self.client.initializer()
        self.currdir = os.getcwd()

    def test_face_frame_only(self):
        #face_path = os.path.join(self.currdir, "faces")
        face_path = "tests/faces"

        files = [os.path.join(face_path, f) for f in os.listdir(face_path) if os.path.isfile(os.path.join(face_path, f))]

        for file in files:
            json = self.client.detect(image = open(file, 'rb'))

            self.assertEqual(json.get('error_message'), None)
        return
