
'''
Sources: 
(1) https://realpython.com/face-detection-in-python-using-a-webcam/
(2) https://stackoverflow.com/questions/36242860/attribute-error-while-using-opencv-for-face-recognition
(3) https://theailearner.com/2018/10/15/extracting-and-saving-video-frames-using-opencv-python/
(4) https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
'''
import sys
import os
import cv2
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mosquitto", 1883, 60)

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

folder = 'images'

video_capture = cv2.VideoCapture(1)

#iterate for frame labeling
i=0

while True:
    # Capture frame-by-frame every second
    
    ret, frame = video_capture.read()
    #video_capture.set(cv2.CAP_PROP_POS_MSEC,(i*1000))
    #video_capture.set(cv2.CAP_PROP_FPS, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #added to crop image
        sub_face = gray[y:y+h, x:x+w]
        # cv2.imwrite(os.path.join(folder,'test2_'+str(i)+'.jpg'), sub_face)
        img_str = cv2.imencode('.png',sub_face)[1]
        msg = img_str.tobytes()

        #publish
        client.publish(topic = "image", payload = msg, qos=0)
        client.loop(5)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    #Save frame
    if ret == False:
        break
    #cv2.imwrite('test2_'+str(i)+'.jpg', frame)
    #cv2.imwrite(os.path.join(folder,'test2_'+str(i)+'.jpg'), sub_face)
    i+=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()