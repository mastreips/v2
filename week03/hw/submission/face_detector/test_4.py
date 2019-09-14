'''
Author: Marcus A. Streips

This is a simple test script that sends a single image to a message broker. 

'''
import cv2
import paho.mqtt.client as mqtt

img = 'test2_175.jpg'


fileContent = cv2.imread(img)  # Read image using CV library

#Create MQTT publication client
client = mqtt.Client()  
client.connect("172.18.0.1", 1883, 60)

#Convert image to byte array format in order to send via MQTT protocol. 
img_str = cv2.imencode('.jpg',fileContent)[1]
msg = img_str.tobytes()

#Publish image to MQTT "image" topic using QoS send at least once protocol, requiring confirmation of receipt from broker.
client.publish(topic = "image", payload = msg, qos=1)
