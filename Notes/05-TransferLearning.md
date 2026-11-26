# Transfer Learning

## Intro to Transfer Learning

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/1-5.jpg"/>
</p>

> Deep learning vs. transfer learning: training from scratch means learning features and training a classifier on a large public dataset, which takes hours or days. Transfer learning reuses those learned features without new training and only trains a classifier on a small local dataset, which takes minutes.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/2-3.jpg"/>
</p>

> Training Models: these models can be saved and deployed for the world to use. Training these models require a large amount of computing resources and dollars. Let's rather use models that have already been created and build our apps by piggy backing.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/2-4.jpg"/>
</p>

> Transfer Learning: These models are robust, and have been tested in detail and perform extremely well. We can take the patterns (also called weights) that another model has learned from a different use case and use it solve our own problem. We could also take the patterns from a language model (a model that's been through large amounts of text to learn a representation of language) and use them as the basis of a model to classify different text samples.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/2-5.jpg"/>
</p>

> We can leverage an existing model (a neural network architecture) proven to work on problems like our own. We can leverage a working model which has already learned patterns on similar data to our own. This often results in achieving great results with less custom data from available small datasets.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/2-6.jpg"/>
</p>

> A study into the effects of whether training from scratch or using transfer learning was better from a practitioner's point of view found transfer learning to be far more beneficial in terms of cost and time. Suddenly lots more people can do world-class work with less resources and less data

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/2-7.jpg"/>
</p>

> Finetuning: the first way to use pretrained models in CNN applications. Instead of random initialization, we initialize the network with a pretrained network. However, we unfreeze some or all pre-trained layers to update their weights on new data. Thus, the rest of the training looks as usual.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/2-8.jpg"/>
</p>

> Feature Extraction: the second way to use pretrained models in ConvNet applications. Here, we will freeze the weights for all the Convolution layers. The last or last few fully connected layers are replaced with a new one with random weights and trained.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-2.jpg"/>
</p>

> Feature Extraction with EfficientNetB0: the backbone pretrained on ImageNet stays the same (frozen), and only the final linear classifier layer (`torch.nn.Linear`) changes. Its output shape matches the number of new classes.

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/2-10.jpg"/>
</p>

> In the picture above, we freeze all the layers or parameters in the features section of this `efficientnet_b0` model. Freeze means the weights are not trainable OR as we know it `require_grad = False`. When using a pretrained model, it's important that your custom data going into the model is pre-processed and normalized in the same way as the original training data that went into the model.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-1.jpg"/>
</p>

> Convolutional Neural Network (CNN): the input image passes through repeated convolution and pooling layers that build up feature maps (feature extraction). The final feature maps are flattened into a fully connected layer that outputs a probability distribution over the classes (here Tweety at 0.7). In transfer learning, the feature extraction part is what we reuse.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/1-6.jpg"/>
</p>

> Freezing vs. fine tuning: a network pretrained on a large labeled dataset is transferred to a similar task with a small labeled dataset. Its convolutional layers are frozen, while the final fully connected and sigmoid layers are fine tuned. The table shows what to do based on dataset size and similarity. With a small dataset, train a classifier on the highest level features (similar data) or only the lower level features (different data). With a large dataset, fine tune either way.

## Worked Examples

### Cost Function (Mean Squared Error)

The cost function measures how far a model's predictions are from the true values:

$$
J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} \left( h_\theta(x_i) - y_i \right)^2
$$

- $h_\theta(x_i)$ is the model's prediction for sample $i$, and $y_i$ is the true value
- Squaring removes negative errors so they can't cancel out positive ones
- Dividing by $m$ takes the mean, so the cost doesn't grow just because there are more samples
- The $\frac{1}{2}$ is there to make the math cleaner when taking the derivative during training

**Example:** 3 samples with predictions $(2, 4, 6)$ and true values $(3, 4, 8)$

| Sample | Prediction | True value | Error | Error² |
|---|---|---|---|---|
| 1 | 2 | 3 | −1 | 1 |
| 2 | 4 | 4 | 0 | 0 |
| 3 | 6 | 8 | −2 | 4 |

$$
J = \frac{1}{2 \times 3}(1 + 0 + 4) = \frac{5}{6} \approx 0.833
$$

### ImageNet Input Normalization

Torchvision's pretrained models expect mini batches of 3 channel RGB images shaped $(3 \times H \times W)$, where $H$ and $W$ are at least 224. Each pixel is first scaled from $[0, 255]$ to $[0, 1]$, then normalized per channel with ImageNet's mean and standard deviation:

$$
x_{norm} = \frac{x - \text{mean}_c}{\text{std}_c}
$$

| Channel | Mean | Std |
|---|---|---|
| Red | 0.485 | 0.229 |
| Green | 0.456 | 0.224 |
| Blue | 0.406 | 0.225 |

**Example:** a red channel pixel with value 200

$$
\frac{200}{255} \approx 0.784 \quad \rightarrow \quad \frac{0.784 - 0.485}{0.229} \approx 1.307
$$

Your custom images must go through these exact steps, because the pretrained weights were learned on data prepared this way.
