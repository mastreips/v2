## W251 
## Marcus A. Streips

# Homework 3 - Internet of Things 101

## Requirements 
Please point us to the repository of your code and provide an http link to the location of your faces in the object storage.  
Also, explan the naming of the MQTT topics and the QoS that you used.

## Submitted Files

### Cloud Services
- cloud COS/mqtt_sub_test1.py   (subscription routing that writes to s3fs-fuse mounted object storage)
- cloud COS/mqtt_sub_test4.py   (subscription routing that writes to ibm COS using ibm3_boto library)

### Jestson - Face Detetion Service
- face_detector/vid_cap_test5.py  (face detection and clipping service connected to mqtt broker)
- face_detector/test_4.py   (testing script for sending a single message to the broker). 

### Jetson - Forwarder Service
- forwarder/mosquitto.conf (configuration file for mosquitto bridge)
- forwarder/mqtt_forwarder_test1.py (forwarding service that subscribes to local broker and publishes to remote broker)

### Miscellaneous
- image_examples/test2_92.jpg (screencap of video displayed during face capture)
- image_examples/test2_161.jpg (screencap of clipped, gray scale image obtained from face detection service)

## Link to COS Bucket

- Link to Bucket (mastreipsbucket1) - This link may not work (Bad Gateway). I have provided Dima, Brad, Darragh and Esteban with access to my COS bucket: mastreipsbucket1.

filter by "test" prefix to see images

https://cloud.ibm.com/objectstorage/crn%3Av1%3Abluemix%3Apublic%3Acloud-object-storage%3Aglobal%3Aa%2F42fc791bbc1f45c4bf6747a763dc4206%3A5ebcf782-1986-4370-9079-11ea8b762910%3A%3A?bucket=mastreipsbucket1&bucketRegion=us-east&endpoint=s3.us-east.cloud-object-storage.appdomain.cloud&paneId=bucket_overview

## Overview
The purpose of this projet to to use mqtt and docker to capture facial images and send messages through brokers to on IBM Cloud Object Storage (COS) bucket. 

Two different approaches for linking Jetson to the Cloud were explored.  The first approach used the Jetson mosquitto broker as a bridge to the cloud broker.  The second approach used the paho-mqtt wrapper as a forwarder.  

Two different approaches for storing the images where explored. The first approach connected the docker image to an s3fs-fuse object storage drive and wrote to the drive using standard python IO commands.  The second approach used the ibm3_boto library to connect to COS through API endpoints.  Only the second approach resulted in a UI with updated objects and is accessible using the link above. 

### Topics - 

**Bridge**
- Using the mosquitto bridge I used MQTT topic "#" so that I would transmit all messages during testing.
- Messages were sent using QoS 0. This guarantees best effort delivery which does not require confirmation of reciept.  This is a good mode for efficiency, where speed is more important that data loss prevention.  Given the number of 10k images being sent ove the wire, I thought this was a better choice. 

**Forwarder**
- Using the paho-mqtt service I used MQTT topic "image" to identify images sent by the face detection service
- Messages where sent using QoS 1. The sender stores message until it gets a PUBBACK notice from the receiver acknowledging response. This mode ensures delivery, but does not guarantee duplications.  I used this method as an alternative to QoS 0 on the bridge to compare perfomrance.  It did seem less fast, but this could also be due to the overhead of the paho-mqtt wrapper which the bridge does not have. 

## Mosquitto log (Bridge)
```
1567960903: mosquitto version 1.6.3 starting
1567960903: Config loaded from /etc/mosquitto/mosquitto.conf.
1567960903: Opening ipv4 listen socket on port 1883.
1567960903: Opening ipv6 listen socket on port 1883.
1567960903: Bridge local.7f6ddfcca007.hw3_mosquitto_bridge doing local SUBSCRIBE on topic #
1567960903: Connecting bridge hw3_mosquitto_bridge (52.117.212.167:1883)

1567960991: Received PUBLISH from auto-3BEC3539-23B4-0477-5AD2-0A8691302111 (d0, q0, r0, m0, 'image', ... (9070 bytes))
1567960991: Sending PUBLISH to local.7f6ddfcca007.hw3_mosquitto_bridge (d0, q0, r0, m0, 'image', ... (9070 bytes))
1567960991: Received PUBLISH from auto-3BEC3539-23B4-0477-5AD2-0A8691302111 (d0, q0, r0, m0, 'image', ... (8541 bytes))
1567960991: Sending PUBLISH to local.7f6ddfcca007.hw3_mosquitto_bridge (d0, q0, r0, m0, 'image', ... (8541 bytes))
```

## Forwarder log
```
1567975709: mosquitto version 1.4.15 (build date Tue, 18 Jun 2019 11:42:22 -0300) starting
1567975709: Using default config.
1567975709: Opening ipv4 listen socket on port 1883.
1567975709: Opening ipv6 listen socket on port 1883.
1567975733: New connection from 75.190.38.102 on port 1883.
1567975733: New client connected from 75.190.38.102 as forwadrer_remote (c1, k60).
1567975733: Sending CONNACK to forwadrer_remote (0, 0)
1567975779: Received PUBLISH from forwadrer_remote (d0, q1, r0, m1, 'image', ... (8004 bytes))
1567975779: Sending PUBACK to forwadrer_remote (Mid: 1)
```

## Cloud Docker Commands
`docker run -it --name img_proc --privileged ubuntu   (needed to mount fuse disk by docker container "ubuntu")`

## Jestson Docker Commands
`docker run -it --rm --net=hw03 --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --device=/dev/video1 --name face_detector_2 w251/cuda:dev-tx2-4.2.1_b97 (needed to access display by docker container)`

## Jetson Network 
```
[
    {
        "Name": "hw03",
        "Id": "75c8472a5365bfa883788453ce3a591ffc9f14cbaf866352d97494394b5ea27c",
        "Created": "2019-09-05T14:48:02.241991846-04:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "6979acf71066bd562ea0a308a347588b3d01d322eed8e7d3a438e32eaa0265c0": {
                "Name": "forwarder",
                "EndpointID": "6f1c652aef583fa5725b3db4f91fe9e8f8b58e077bbc3aa3e0b110c88b701442",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            },
            "712abb7d9cbfb3a1be4f8c62113022922a18db74aecd1891e3b5f19ebc24e02a": {
                "Name": "face_detector_2",
                "EndpointID": "bf8f85755c624a446def19c4cce1e1437ebfe87bcc0dbab771030ab3417ba7b2",
                "MacAddress": "02:42:ac:12:00:05",
                "IPv4Address": "172.18.0.5/16",
                "IPv6Address": ""
            },
            "7f6ddfcca007f02fc855c8e287d82e12979caf96a502980e8d451f5d504d816e": {
                "Name": "mosquitto",
                "EndpointID": "d9f7fda52e8dc8738f5e038a32ec439218747b2bc54fe52b1a7ab4c8dd491e1b",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

## Cloud Network
```
[
    {
        "Name": "hw03_cloud",
        "Id": "93e4fdf160b9e11550062c4e7ac5e8d0a44b3234b47e8ebf7b614e9daa0aa10c",
        "Created": "2019-09-07T02:09:32.041727057Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "4d274686e083bbd11169d4e9990fc7a74926e4c40eab7be8090816f93677fa9d": {
                "Name": "mosquitto_cloud",
                "EndpointID": "c0b8dc8fa57f9a9a734a4383fce7e9a8ed2c898bf73a5c537a86197878ea2343",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            },
            "6b4d88681e95da503a33bf6eb454bec585e53784f894e7368ee2801bc0dfe1e4": {
                "Name": "img_proc",
                "EndpointID": "7d0e7ae0140702f469e9fb62c0937a1e657917512f450745d066231d45682d8c",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```
