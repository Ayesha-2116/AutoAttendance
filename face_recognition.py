import face_recognition
import cv2
import os
import numpy as np
from pymongo import MongoClient
import base64
from io import BytesIO

client = MongoClient('mongodb://localhost:27017/')
db = client['attendance']
collection = db['students']

# Initialize a variable to store the reference face encodings and student IDs
known_face_encodings = []
student_ids = []
student_names = []
# Load known faces and their encodings from MongoDB
students = collection.find()

for student in students:    
    name = student['name']
    student_id = student['student_id']
    photo_data = student['photo']
    # Decode the base64 photo data
    image_bytes = base64.b64decode(photo_data)
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    # Get the face encoding
    face_encodings = face_recognition.face_encodings(image)
    
    if face_encodings:
        known_face_encodings.append(face_encodings[0])
        student_ids.append(student_id)
        student_names.append(name)
    else:
        print(f"No face found in the photo for student ID {student_id}")

# Start the video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    # Resize frame for faster processing (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Find face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)
    
    for face_encoding in face_encodings:
        # Compare the face with the known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        # Find the distances to all known faces
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        # Get the best match index
        best_match_index = face_distances.argmin()
        
        if matches[best_match_index]:
            student_id = student_ids[best_match_index]
        else:
            student_id = "Unknown"

        # Print the student ID on the frame
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, student_id, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
video_capture.release()
cv2.destroyAllWindows()