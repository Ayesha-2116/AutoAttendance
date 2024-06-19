import face_recognition
import cv2
import os

# Path to the dataset folder
dataset_path = "dataset"

# Initialize a dictionary to hold the encodings and student IDs
known_encodings = []
student_ids = []

# Load and encode each student image
for file_name in os.listdir(dataset_path):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        # Get the student ID from the file name (assuming it's the name without the extension)
        student_id = os.path.splitext(file_name)[0]

        # Load the image file
        image_path = os.path.join(dataset_path, file_name)
        student_image = face_recognition.load_image_file(image_path)

        # Get the face encoding
        student_encoding = face_recognition.face_encodings(student_image)[0]

        # Append the encoding and student ID to the lists
        known_encodings.append(student_encoding)
        student_ids.append(student_id)
print(student_ids)
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
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        
        # Find the distances to all known faces
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        
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