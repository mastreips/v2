
'''
Sources: 
(1) https://realpython.com/face-detection-in-python-using-a-webcam/
(2) https://stackoverflow.com/questions/36242860/attribute-error-while-using-opencv-for-face-recognition
(3) https://theailearner.com/2018/10/15/extracting-and-saving-video-frames-using-opencv-python/
(4) https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames

Author: Marcus A. Streips

This script uses the OpenCV and paho.mqtt libraries to detect and capture frames of facial features captured on a live video 
steam, store them in memory as byte arrays and send them to a MQTT message broker. 

'''
import sys
import os
import cv2
import paho.mqtt.client as mqtt

#Create mqtt publishing client
client = mqtt.Client()
client.connect("mosquitto", 1883, 60)

#library for detecting facial features using Haar Cascades
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

folder = 'images'

#Begin capturing video via WebCam on USB port 1
video_capture = cv2.VideoCapture(1)

#iterate for frame labeling
i=0

while True:
   
    ret, frame = video_capture.read()                       # Capture each frame of the video  

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          # Turn captured frame into grayscale to reduce image size

    # use faceCascade method to detect facial features in the frame
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #added to crop image
        sub_face = gray[y:y+h, x:x+w]
        
        # cv2.imwrite(os.path.join(folder,'test2_'+str(i)+'.jpg'), sub_face)  #write to disk for testing purposes
        
        # save clipped image into memory as a byte arrar
        img_str = cv2.imencode('.png',sub_face)[1]
        msg = img_str.tobytes()

        #publish to broker using QoS = 0 protocol which does not require confirmation to increase processing speed.
        client.publish(topic = "image", payload = msg, qos=0)
        client.loop(5)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    #Save frame
    if ret == False:
        break
    #cv2.imwrite('test2_'+str(i)+'.jpg', frame)                             #write to disk for testing purposes
    #cv2.imwrite(os.path.join(folder,'test2_'+str(i)+'.jpg'), sub_face)     #write to disk for testing purposes
    i+=1

    # Quit process upon pressing 'q' on keyboard 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
