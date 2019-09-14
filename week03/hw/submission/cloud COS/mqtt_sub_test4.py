'''
Sources:
(1) cloud.ibm.com/docs/services/cloud-object-storage
(2) http://stackoverflow.com/questions/37499739/how-can-i-send-a-image-by-using-mosquitto

Author: Marcus A. Streips

This script uses the ibm_boto3 script and paho.mqtt python MQTT wrapper to capture messages from a MQTT broker and write 
them to a bucket in the IBM Cloud Object Store (COS).  The script assignes a GUID to each message to make sure they are 
recorded as unique records.  

'''

import paho.mqtt.client as mqtt
import uuid
import ibm_boto3
from ibm_botocore.client import Config, ClientError

## IBM Cloud Credentialing 
credentials = {
  "apikey": "",
  "cos_hmac_keys": {
    "access_key_id": "",
    "secret_access_key": ""
  },
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key f234366a-073c-481e-a7f9-ab1c1bf95e65",
  "iam_apikey_name": "Service credentials-2",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/42fc791bbc1f45c4bf6747a763dc4206::serviceid:ServiceId-c2ae7508-1108-4c07-9ab3-a6270706bc8f",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/42fc791bbc1f45c4bf6747a763dc4206:5ebcf782-1986-4370-9079-11ea8b762910::"
}

auth_endpoint = "https://iam.cloud.ibm.com/identity/token"
service_endpoint = "https://s3.us-east.cloud-object-storage.appdomain.cloud"
bucket = "mastreipsbucket1"


## connect function for subscribing to all channels on the broker 
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	
	client.subscribe("#")  		# subscribe to all channels / all messages
	#client.subscribe("image")	# subscribe only to image channels. Turned off for testing purposes. 

## message writing function used to assign GUID and write message to IBM COS instance	
def on_message(client, userdata, msg):

	print("Topic : ", msg.topic + "\n Image : " +  msg.payload)
	i = str(uuid.uuid4())  # Create GUID for each message
	print(i)

	png_name = "output_%s.png" % i
	resource.Bucket(name=bucket).put_object(Key=png_name, Body=msg.payload)  #use ibm_boto3 object to write to storage
	print("wrote to bucket")

## Instantiate ibm_boto3 resource object
resource = ibm_boto3.resource('s3', 
	ibm_api_key_id = credentials['apikey'],
	ibm_service_instance_id = credentials['resource_instance_id'],
	ibm_auth_endpoint  = auth_endpoint,
	config=Config(signature_version='oauth'),
	endpoint_url = service_endpoint)

# Create MQTT subscription client
client = mqtt.Client()
client.on_connect =  on_connect
client.on_message = on_message
client.connect("172.18.0.1", 1883)		# Connect to the Docker Gateway Address
##client.connect("172.18.0.2", 1883, 60)	# Connect to the Docker Subnet Address
client.loop_forever()
