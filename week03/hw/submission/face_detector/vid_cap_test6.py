 
import numpy as np
import cv2
import paho.mqtt.client as mqtt

broker_address = "172.18.0.1"
client = mqtt.Client("face")
client.connect(broker_address)

cap = cv2.VideoCapture(1)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # when faces are found print coordinates and display cropped image for debugging purposes
    # then publish to mqtt
    for (x,y,w,h) in faces:
        print(x,y,w,h)
        crop_img = frame[y:y+h, x:x+w]
        cv2.imshow("cropped", crop_img)
        client.publish("image", cv2.imencode('.png',crop_img)[1].tobytes())

    # display live video feed for debugging purposes 
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
