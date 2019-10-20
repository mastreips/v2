## Homework 9 ##

How long does it take to complete the training run? (hint: this session is on distributed training, so it will take a while)

**ANS:  50k step in 22 hours, 12 minutes, 10 seconds (according to Tensorboard)**


Do you think your model is fully trained? How can you tell?

**ANS: The model is getting close to being fully trained at 50K steps as its BLEU score is 0.3691 and the example with 300k steps
had a BLEU score of 0.380.**

![Model BLEU Score 0.3691](images/TensorBoard_BLUE.png)

Were you overfitting?

**ANS: No. Both Eval and Training Losses are consistently decreasing.
If the model was overfitting we would see a divergence.**

![Model Eval Loss](images/TensorBoard_eval_loss.png)

![Model Train Loss](images/TensorBoard_train_loss.png)


Were your GPUs fully utilized?

**ANS: Yes. All Cores of Both GPUs at each node was 100%
utilized**

![GPU v100a](images/gpuv100a.png)

![GPU v100a](images/gpuv100b.png)

Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?

**ANS: Yes. I did monitor the network.  The eth0 network was running around 200 Mb/s and the network is configured for 
1000 Mb/s (1Gb/s). The network was not the bottleneck.  Given that all GPUs were running at 100% it is likely that the 
GPUs where the bottleneck in this run.**

![network](images/network.png)