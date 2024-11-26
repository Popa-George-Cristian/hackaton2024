import cv2

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/proiect/haarcascade_frontalface_default.xml')

# Initialize the LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the training data
recognizer.read('training_data.yml')

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a frame from the video
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Process each detected face
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Perform face recognition
        label, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Determine the label name based on confidence
        if confidence < 100:
            name = f"Person {label}"
        else:
            name = "Unknown"

        # Display the label on the video feed
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show the resulting frame
    cv2.imshow('Face Recognizer', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up resources
video_capture.release()
cv2.destroyAllWindows()
