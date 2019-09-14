'''
Sources: 
(1) http://stackoverflow.com/questions/37499739/how-can-i-send-a-image-by-using-mosquitto

Author:  Marcus A. Streips

This script uses paho.mqtt to create a subscription and writting service that listens for messages coming into an MQTT broker 
and writes them to an instance of a mounted s3fs-fuse object storage disk using the classic IBM cloud infrastructure.  The 
script assigns a GUID to each method to ensure they are saved as unique records and uses standard Python IO commands to write
to the mounted fuse object. 

'''

import paho.mqtt.client as mqtt
import uuid

# Function for creating the broker subscription service
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	
	client.subscribe("#")		# listen too all incoming messages
	#client.subscribe("image")	# listen to only messages tagged as "image". Turned off for testing purposes. 

# Function for creating the message writing service
def on_message(client, userdata, msg):

	print("Topic : ", msg.topic + "\n Image : " +  msg.payload)
	i = str(uuid.uuid4())	# Assign GUID to each method
	print(i)
	f = open("/mnt/mybucket/output_%s.png" % i, "wb") #Write message as binary to convert back to image format
	f.write(msg.payload)
	f.close()

# Create subscription and writting client
client = mqtt.Client()
client.on_connect =  on_connect
client.on_message = on_message
client.connect("172.18.0.1", 1883)		# Connect to Docker Network Gateway IP
##client.connect("172.18.0.2", 1883, 60)	# Connect to Docker Container Subnet IP
client.loop_forever()
