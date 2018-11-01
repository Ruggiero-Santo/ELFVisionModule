import unittest
import pytest
import cv2
import os
from API_Class import FacePlusPlus


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = FacePlusPlus()
        self.client.setAttr()

    def test_face_frame_only(self):
        face_path = "tests/faces"

        files = [os.path.join(face_path, f) for f in os.listdir(face_path) if os.path.isfile(os.path.join(face_path, f))]

        for file in files:
            json = self.client.detect(file = file)
            self.assertEqual(json.get('error_message'), None)
        return

    def test_detect_with_path(self):
        face_path = "tests/faces"

        files = [os.path.join(face_path, f) for f in os.listdir(face_path) if os.path.isfile(os.path.join(face_path, f))]

        for file in files:
            json = self.client.detect(file = file)
            self.assertEqual(json.get('error_message'), None)
        return


    def test_attributes_changes(self):

        self.client.__init__()
        self.assertEqual(self.client.url_params['return_attributes'], "emotion" )

        self.client.setAttr("gender,age,smiling,facequality,blur,eyestatus")
        self.assertEqual(self.client.url_params['return_attributes'], "gender,age,smiling,facequality,blur,eyestatus" )

        with pytest.raises(TypeError):
            self.client.setAttr(1)
