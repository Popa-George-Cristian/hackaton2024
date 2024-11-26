from picamera2 import Picamera2
import cv2

# Initialize the camera
picam2 = Picamera2()
picam2.start()

while True:
    frame = picam2.capture_array()  # Capture a frame as NumPy array
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)    
    # Display the captured frame using OpenCV
    cv2.imshow("Camera Feed", frame_bgr)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
