from picamera2 import Picamera2
import cv2, dlib, face_recognition

cv2.ocl.setUseOpenCL(True)
print("OpenCL Enabled:", cv2.ocl.useOpenCL()) 

picam2 = Picamera2()
picam2.start()

cam = cv2.VideoCapture(0)

predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
detector = dlib.get_frontal_face_detector()

load_image = face_recognition.load_image_file('./images/cercel.jpg')
load_image_2 = face_recognition.load_image_file('./images/gabi.jpg')
load_image_3 = face_recognition.load_image_file('./images/anisia.jpg')

image_cercel = face_recognition.face_encodings(load_image)[0]
image_gabi = face_recognition.face_encodings(load_image_2)[0]
image_anisia = face_recognition.face_encodings(load_image_3)[0]
known_face_encodings = [image_cercel, image_gabi, image_anisia]
known_face_names = ["Cercel", "Gabi", "Anisia"]

while True:
    frame = picam2.capture_array()
    # ret, frame = cam.read()
    frame_color_normal = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(frame_color_normal)
    face_encodings = face_recognition.face_encodings(frame_color_normal, face_locations)
        
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        cv2.rectangle(frame_color_normal, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame_color_normal, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame_color_normal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
