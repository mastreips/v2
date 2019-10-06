# Homework 7 - Neural face detection pipeline

### Overview
The objective of this homework is simple: modify the processing pipeline that you implemented in 
[homework 3](https://github.com/MIDS-scaling-up/v2/blob/master/week03/hw/README.md) and replace the OpenCV-based face detector with 
a Deep Learning-based one. You could, for instance, rely on what you learned in 
[TensorRT lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_tensorrt.md) or 
[Digits lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_digits.md)

### Hints
* You have the freedom to choose the neural network that does the detection, but don't overthink it; this is a credit / no credit assignment that is not supposed to take a lot of time.
* There is no need to train the network in this assignment, just find and use a pre-trained model that is trained on a face dataset.
* Your neural detector should run on the Jetson.
* Just like the OpenCV detector, your neural detector needs to take a frame as input and return an array of rectangles for each face detected.
* Most neural object detectors operate on a frame of a given size, so you may need to resize the frame you get from your webcam to that resolution.
* Note that face detection is not the same as face recognition; you don't need to discriminate between different faces
* Here's a [sample notebook](hw07-hint.ipynb) that loads and uses [one face detector](https://github.com/yeephycho/tensorflow-face-detection)
* A more graceful solution would involve using a face detector from [TensorFlow's Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) -- [this network](http://download.tensorflow.org/models/object_detection/facessd_mobilenet_v2_quantized_320x320_open_image_v4.tar.gz), to be exact, but at the moment, simply loading it as we did in [TensorRT lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_tensorrt.md)  does not work due to [this bug](https://stackoverflow.com/questions/53563976/tensorflow-object-detection-api-valueerror-anchor-strides-must-be-a-list-wit)

### Questions
* Describe your solution in detail.  What neural network did you use? What dataset was it trained on? What accuracy does it achieve?

I used the TensorRT Dockerfile with the following command:

```
docker run --privileged --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --device=/dev/video1 -p 8888:8888 --name tensorrtlab05 --net=hw07 -d facecap 
```
I used the frozen_inference_graph_face.pb neural network after running the following command to make it part of my local docker container:

```
!wget https://github.com/yeephycho/tensorflow-face-detection/blob/master/model/frozen_inference_graph_face.pb?raw=true -O {FROZEN_GRAPH_NAME}
```
The model is mobilenet SSD(single shot multibox detector) based face detector with pretrained model provided, powered by tensorflow object detection api, trained on the WIDERFACE dataset. Depending on which mobilenet model it was trained on, it will achieve between 82 and 92% accuracy (see: https://github.com/tensorflow/models/tree/master/research/slim).  

I had a second apline docker container running the mosquitto broker on this network:

```
[
    {
        "Name": "hw07",
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
            "7f6ddfcca007f02fc855c8e287d82e12979caf96a502980e8d451f5d504d816e": {
                "Name": "mosquitto",
                "EndpointID": "beb747143f0fbb6d9f6e0afc325d384c901e16b621041b02b190533fd7262931",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            },
            "c27893a814966076698ef593907136bd9e681e1318d343baca8a6d5741280504": {
                "Name": "facecap",
                "EndpointID": "ac3c647bd03cfd12ce0b33a5661d8395f0990087d1b998803e2e296ed57e1eb6",
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

I used the following mqtt bridge configuration:

```
connection hw7_mosquitto_bridge
address 52.116.242.42:1883
cleansession true
try_private false
log_type all
#log_dest file /var/log/mosquitto/mosquitto.log
topic # out 0
```
I had a separate broker running on an Ubuntu VM in the cloud that was using a paho.mqtt script to subscribe to the "image" topic and write to an IBM COS bucket with the following URL: 

https://cloud.ibm.com/objectstorage/crn%3Av1%3Abluemix%3Apublic%3Acloud-object-storage%3Aglobal%3Aa%2F42fc791bbc1f45c4bf6747a763dc4206%3A5ebcf782-1986-4370-9079-11ea8b762910%3A%3A?bucket=mastreipsbucket1&bucketRegion=us-east&endpoint=s3.us-east.cloud-object-storage.appdomain.cloud&paneId=bucket_overview

* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?

I did not train the model so I cannot answer the question about empirical testing. That said, the model is a well known model, trained on a well-known dataset with .80 - 0.90% accuracy, so I would consider it an appropriate solution for a production-grade system. 

* What framerate does this method achieve on the Jetson? Where is the bottleneck?

The model achieves Frames per second using video.get(cv2.CAP_PROP_FPS) : 30.0.  The bottleneck is the ability of the Jetson GPU/CPU to process the images. 

* Which is a better quality detector: the OpenCV or yours?

The MobileNet TensorRT model is the better detector as it could pick up my facial features instantly at various angles and distances.  The OpenCV Haar based model had difficulty detecting my face unless it was appropriately centered. 

### To turn in:

Please provide answers to questions above, a copy of the code related to the neural face detector along with access to the location (object storage?) containing the detected face images. Note that this homework is NOT graded, credit / no credit only.
