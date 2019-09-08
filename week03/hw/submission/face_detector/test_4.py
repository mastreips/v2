import cv2
import paho.mqtt.client as mqtt

img = 'test2_175.jpg'

#f = open(img, "rb")
#fileContent = f.read()

fileContent = cv2.imread(img)


client = mqtt.Client()
client.connect("172.18.0.1", 1883, 60)


img_str = cv2.imencode('.jpg',fileContent)[1]
msg = img_str.tobytes()

client.publish(topic = "image", payload = msg, qos=1)
