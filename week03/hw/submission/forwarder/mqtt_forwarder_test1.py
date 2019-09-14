'''
Sources:
(1) http://www.steves-internet-guide.com/client-connections-python-mqtt/

Author: Marcus A. Streips

This forwarer script subscribes to the 'image' channel on a local MQTT broker and transmits ("forwards) the message to a 
remote broker instance. It is essentially a relay.  This script was used as an alternative to setting up the local MQTT broker
as a bridge to the remote broker instance.  The config file for the bridge is found in this directory for comparison purposes.
'''

import paho.mqtt.client as mqtt

# MQTT network information
local_broker_address = "172.18.0.2"
remote_broker_address = "52.117.212.167"
topic = "image"

# Function to create a local subscription service
def on_connect_local(client, userdata, flags, rc):
	print("connected to local broker")
	client.subscribe(topic)

# Function to create a publishing service
def on_message(client, userdata, msg):
	remote_client.publish(topic, payload=msg.payload, qos=1, retain=False)

# Create instance of subscription service 
local_client = mqtt.Client(client_id = "forwadrer_local", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport='tcp')
local_client.on_connect = on_connect_local
local_client.connect(local_broker_address)
local_client.on_message = on_message

# Create instance of publication service connecting to Cloud
remote_client = mqtt.Client(client_id = "forwadrer_remote", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport='tcp')
remote_client.connect(remote_broker_address, 1883)

local_client.loop_forever()
