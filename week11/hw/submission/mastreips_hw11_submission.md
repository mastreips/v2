# Homework 11 -- Marcus Streips

## Baseline

A baseline was run using the default configuration.  The run-time was approximately 3 hours:

```
#baseline run
def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dense(1))
    #model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=[mean_squared_error])
    return model

```


Link to Video - https://s3.us-east.cloud-object-storage.appdomain.cloud/mastreipsbucket1/baseline_frame50000.mp4


## Second Run

The default configuration was changed to change the activation layer to 'relu', and to increase the size of the two layers, along with changing the optimize to adamax. The run-time was approximately 3 hours. The result was only a small improved observed improvement in the perfomance of the model. 

```
#Second Run
def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=adamax(lr=0.001), metrics=[mean_squared_error])
    return model
```

Link to Video - https://s3.us-east.cloud-object-storage.appdomain.cloud/mastreipsbucket1/second_run_frame50000.mp4

## Third Run

The size of the layers was increased, which resulted in a memory error, as such the size of the training run threshold was reduced to 1000 and the total_iters was raised to 100000.  By reducing the training threshold, enough memory was available for the model to run a much larger network (150, 120). The optimizer was changed back to adam and the configuration was optimized using parameters from research literature.  The approximate run-time was 24 hours.  

Only a slight improvement was observed in the performance of the model. The lander would do a good job controlling its decent, but had difficulty with lateral adjustments. 

```
# run_lunar_lander.py changes

    #training_thr = 3000 #trials 1 and 2
    training_thr = 2000
    # total_itrs = 50000 #trials 1 and 2
    # total_itrs = 100000 # trial 3
    total_itrs = 350000 # trial 4
    successful_steps = []

     if steps > training_thr and steps %1000 ==0:
            # re-train a model
            print("training model model")
            # print("X_train", X_train)
            # print("y_train", y_train)
            modelTrained = True
            model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 20, batch_size=20) #was 10


# lunar_lander.py changes

# Third Run
# Ref: (1) http://machinelearningmastery.com/adam-optimization-algorithm-for-deep-learning

def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(150, input_dim=input_dim, activation='relu'))
    model.add(Dense(120, activation='relu'))
    model.add(Dense(1))
    #model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.compile(loss='mean_squared_error', optimizer=adam(lr=0.001, beta_1=0.9, beta_2=0.996), metrics=[mean_squared_error])
    return model

```

Link to Video - https://s3.us-east.cloud-object-storage.appdomain.cloud/mastreipsbucket1/third_run_frame100000.mp4

### Third-Run Statitics
```
Epoch 10/10
100001/100001 [==============================] - 23s 229us/step - loss: 
284.9012 - mean_squared_error: 284.9010
At step  100000
reward:  -36.86963856290388
total rewards  82.12761390829894

Total successes are:  220

```
## Final Run

It was determined that the number of iterations would need to be 350000k + which would take 72+ hours to run.  An initial final run was attempted using CPU alone.  This run failed after running more than 72 hours.  A second attempt was made after making a few adjustments.  First the GPU was enabled using the `export CUDA_VISIBLE_DEVICES="0"` command.  The GPU memory was allowed to grow using the following changes to the lunar_laner.py file:

```
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
```

The batch size was increased from 20 to 64 to allow parallelized (faster) processing and the epoch training count was raised to 20.  The training threshold was increased to 2000 and the steps %operator was increased to 2000 to speed up the processing time (less video IO operations). The process was allowed to run to run to 180000 steps (approx 32 hours).  The process was manually terminated as it was determined that the loss was not improving after 3+ hours of observation. The same net architecure and parameters from the third run, where used in the final run. The purpose of the final run was to optimize the processing speed to see if we could efficiently run a high number of iterations (350k).

The experiment confirmed that increasing the iterations past 100k did not improve performance of the model.

Only a slight improvement was observed in the performance of the model. The lander would do a good job controlling its decent, but had difficulty with lateral adjustments. 

```
# run_lunar_lander.py changes

    #training_thr = 3000 #trials 1 and 2
    training_thr = 2000
    # total_itrs = 50000 #trials 1 and 2
    # total_itrs = 100000 # trial 3
    total_itrs = 350000 # trial 4
    successful_steps = []

    if steps > training_thr and steps %1000 ==0:
    # re-train a model
    print("training model model")
    # print("X_train", X_train)
    # print("y_train", y_train)
    modelTrained = True
    model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 20, batch_size=64) #was 10 and 20


    if steps >= training_thr and steps %2000 == 0: #was 1000
        fname = "/tmp/videos/frame"+str(steps)+".mp4"
        skvideo.io.vwrite(fname, np.array(frames))
        del frames
        frames = []


# lunar_Lander.py

# Final Run
# Ref: (1) http://machinelearningmastery.com/adam-optimization-algorithm-for-deep-learning
# def nnmodel(input_dim):
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(150, input_dim=input_dim, activation='relu'))
    model.add(Dense(120, activation='relu'))
    model.add(Dense(1))
    #model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.compile(loss='mean_squared_error', optimizer=adam(lr=0.001, beta_1=0.9, beta_2=0.996), metrics=[mean_squared_error])
    return model

```
Link to Video - https://s3.us-east.cloud-object-storage.appdomain.cloud/mastreipsbucket1/final_run_frame180000.mp4

### Final-Run Statitics

'''
Epoch 20/20
179001/179001 [==============================] - 41s 229us/step - loss: 
233.9731 - mean_squared_error: 233.9731
At step  179000
reward:  57.294886964652704
total rewards  109.16068801697253

Total successes are:  449
'''