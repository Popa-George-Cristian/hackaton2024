import face_recognition
import cv2
import numpy as np
# from picamera2 import Picamera2
import time
import pickle

class Camera:
    def __init__(self):
        print("[INFO] loading encodings...")

        # Load face encodings from pickle file
        with open("encodings.pickle", "rb") as f:
            data = pickle.loads(f.read())
        self.known_face_encodings = data["encodings"]
        self.known_face_names = data["names"]

        # Initialize the camera
        # self.picam2 = Picamera2()
        # self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
        # self.picam2.start()
        self.cam = cv2.VideoCapture(0)

        # Initialize variables for performance optimization and tracking
        self.cv_scaler = 4  # Resize factor for faster processing
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
        self.status_code = 0
        self.getName = ''

    def process_frame(self, frame):
        """Process the frame for face recognition."""
        # Resize the frame to increase performance
        resized_frame = cv2.resize(frame, (0, 0), fx=(1/self.cv_scaler), fy=(1/self.cv_scaler))

        # Convert the frame from BGR to RGB
        rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        # Find all faces and their encodings
        self.face_locations = face_recognition.face_locations(rgb_resized_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_resized_frame, self.face_locations, model='hog')

        self.face_names = []
        for face_encoding in self.face_encodings:
            # Compare the new face with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            self.face_names.append(name)

        return frame
    
    def update_status(self, status_code):
        """Update the status code from the UI."""
        self.status_code = status_code

    def draw_results(self, frame):
        """Draw results (bounding boxes and names) on the frame."""
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale the face locations back to the original frame size
            top *= self.cv_scaler
            right *= self.cv_scaler
            bottom *= self.cv_scaler
            left *= self.cv_scaler

            # Check the status_code and set the rectangle color accordingly
            if self.status_code == 1:  # Green for allowed
                box_color = (0, 255, 0)  # Green color in BGR
                text_color = (255, 255, 255)  # White text
            elif self.status_code == 0:  # Red for denied
                box_color = (0, 0, 255)  # Red color in BGR
                text_color = (255, 255, 255)  # White text
            else:
                box_color = (0, 255, 255)  # Red color in BGR
                text_color = (255, 255, 255)  # White text

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 3)
            
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left -3, top - 35), (right+3, top), box_color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, text_color, 1)
                
            self.getName = name
        return frame

    def returnName(self):
        print(self.getName)
        return self.getName

    def calculate_fps(self):
        """Calculate frames per second."""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 1:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()
        return self.fps

    def start_recognition(self):
        # frame = self.picam2.capture_array()
        ret, frame = self.cam.read()
        if not ret:
            print("[ERROR] Unable to capture frame.")
            return 0
                # Process the frame
        processed_frame = self.process_frame(frame)

                # Draw results on the frame
        display_frame = self.draw_results(processed_frame)

                # Calculate FPS and display it
        current_fps = self.calculate_fps()
        cv2.putText(display_frame, f"FPS: {current_fps:.1f}", (display_frame.shape[1] - 150, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return display_frame

    # def release_pi(self):
    #     self.picam2.stop()
    
    def release_cv(self):
        self.cam.release()
        cv2.destroyAllWindows()
