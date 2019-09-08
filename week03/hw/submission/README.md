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

### Jetson - Forwarder Service
- forwarder/mosquitto.conf (configuration file for mosquitto bridge)
- forwarder/mqtt_forwarder_test1.py (forwarding service that subscribes to local broker and publishes to remote broker)

### Miscellaneous
- image_examples/test2_92.jpg (screencap of video displayed during face capture)
- image_examples/test2_161.jpg (screencap of clipped, gray scale image obtained from face detection service)


