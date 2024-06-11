from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from .face_utils import recognize_and_check_liveness, is_liveness_detected
import cv2
import numpy as np
import face_recognition

known_face_encodings = []  # Add known face encodings here
# Load an image file of a known person
image_path = r"D:\MAC_SEM_3\Internship\project\autoattend\attendance\images\gur.jpg"
known_image = face_recognition.load_image_file(image_path)

# Extract face encodings
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Add the face encoding to the list of known face encodings
known_face_encodings.append(known_face_encoding)



def generate_frames():
    cap = cv2.VideoCapture(0)
    frame_sequence = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_sequence.append(frame)
        if len(frame_sequence) > 10:
            frame_sequence.pop(0)

        recognized, face_locations = recognize_and_check_liveness(known_face_encodings, frame)
        liveness = is_liveness_detected(frame_sequence)

        if recognized and liveness:
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, 'Recognized', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Not Recognized', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def face_recog_view(request):
    return render(request, 'attendance/video_stream.html')

def face_recog_page(request):
    return render(request, 'attendance/face_recog.html')
