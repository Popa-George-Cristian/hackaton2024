import cv2

# Încarcă clasificatorul Haar Cascade pentru detectarea feței
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Deschide fluxul video de la camera (poți schimba 0 dacă ai mai multe dispozitive video conectate)
cap = cv2.VideoCapture(0)

while True:
    # Capturează fiecare cadru din fluxul video
    ret, frame = cap.read()
    
    # Dacă nu s-a reușit citirea unui cadru, ieși din buclă
    if not ret:
        break
    
    # Convertește cadrul în gri pentru a îmbunătăți performanța detectării
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectează fețele în cadrul imaginei
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Desenează un dreptunghi în jurul fiecărei fețe detectate
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Afișează cadrul cu fețele detectate
    cv2.imshow('Face Detection', frame)
    
    # Ieși din buclă dacă apăși tasta 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Eliberează camera și închide fereastra
cap.release()
cv2.destroyAllWindows()
