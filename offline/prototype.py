#!/bin/python3
import cv2
import dlib
import numpy as np
import uuid

cam = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
shape_pred = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
people = {}
descriptor_distance_threshold = 0.6

while True:
    _, frame = cam.read()
    detected_faces = detector(frame, 1)
    detected_people = {}
    print('--- frame ---')
    print('stored', len(people), 'people')
    for rect in detected_faces:
        shape = shape_pred(frame, rect)
        face_desc = face_rec.compute_face_descriptor(frame, shape)
        face_desc = np.array(face_desc)
        max_distance = float('inf')
        match_id = None
        for person_id, person_desc in people.items():
            distance = np.linalg.norm(person_desc - face_desc)
            if distance < max_distance:
                max_distance = distance
                match_id = person_id
        if max_distance > descriptor_distance_threshold:
            match_id = str(uuid.uuid4())
            people[match_id] = face_desc
        print('detected', match_id, 'with distance', max_distance)
        detected_people[match_id] = rect
    for match_id, rect in detected_people.items():
        cv2.rectangle(frame, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 255, 0))
        cv2.putText(frame, match_id, (rect.left(), rect.top()), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
    print('detected', len(detected_people), 'people')
    cv2.imshow('cam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
