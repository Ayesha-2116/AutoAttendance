import cv2
import face_recognition
import numpy as np

def recognize_and_check_liveness(known_face_encodings, frame):
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            return True, face_locations

    return False, face_locations

def is_liveness_detected(frame_sequence):
    blink_detected = False
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    for frame in frame_sequence:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

        if len(eyes) >= 2:
            blink_detected = True
            break

    return blink_detected
