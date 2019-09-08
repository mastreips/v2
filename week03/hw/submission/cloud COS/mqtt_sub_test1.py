'''
Sources: 
(1) http://stackoverflow.com/questions/37499739/how-can-i-send-a-image-by-using-mosquitto

'''

import paho.mqtt.client as mqtt
import uuid

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	
	client.subscribe("#")
	#client.subscribe("image")

def on_message(client, userdata, msg):

	print("Topic : ", msg.topic + "\n Image : " +  msg.payload)
	i = str(uuid.uuid4())
	print(i)
	f = open("/mnt/mybucket/output_%s.png" % i, "wb")
	f.write(msg.payload)
	f.close()


client = mqtt.Client()
client.on_connect =  on_connect
client.on_message = on_message
#client.connect("localhost",1883)
client.connect("172.18.0.1", 1883)
##client.connect("172.18.0.2", 1883, 60)
client.loop_forever()
