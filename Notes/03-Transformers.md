# Fine-Tuning Pre-Trained Transformers

## Transformer Architecture

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-3.jpg"/>
</p>

> Transformer architecture: the encoder (left) turns input embeddings plus positional encodings into continuous representations through multi-head attention and feed forward layers, each followed by Add & Norm, repeated N times. The decoder (right) takes the outputs shifted right, applies masked multi-head attention, then attends to the encoder's output. A final linear layer and softmax produce output probabilities. Unlike RNNs and CNNs, there is no recurrence or convolution.

## Hugging Face

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-4.jpg"/>
</p>

> Hugging Face Hub: an open source community with over a million pretrained models (text, image, audio, multimodal), tens of thousands of datasets, and the libraries used to work with them (`transformers`, `datasets`, `diffusers`, `accelerate`).

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-5.jpg"/>
</p>

> Loading the Hugging Face token securely: `load_dotenv()` reads the `.env` file in the project folder into environment variables, and `os.getenv("HF_TOKEN")` checks the token loaded. This keeps the token out of the code itself.

## NLP With Pretrained Transformer Models

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-6.jpg"/>
</p>

> Encoder and decoder in the NLP context: the encoder builds a representation (features) of the input, so it is optimized for understanding. The decoder uses those features plus the outputs generated so far (shifted right) to produce a target sequence, so it is optimized for generation. Each part can be used on its own.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-7.jpg"/>
</p>

> Model families by type: encoder only models (ALBERT, BERT, DistilBERT, ELECTRA, RoBERTa) handle sentence classification, named entity recognition, and extractive question answering. Decoder only models (CTRL, GPT, GPT-2, Transformer XL) handle text generation. Encoder decoder models (BART, T5, Marian, mBART) handle summarization, translation, and generative answering.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-8.jpg"/>
</p>

> The 3 step process for NLP apps: raw text ("This course is amazing") goes into the tokenizer, which turns it into input IDs (101 and 102 mark the start and end). The model outputs logits ([-4.3630, 4.6859]), and post processing converts them into predictions.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-9.jpg"/>
</p>

> Starter template for any NLP task: load the tokenizer with `AutoTokenizer` and the model with `AutoModelForSequenceClassification`, both from the same checkpoint (`bert-base-uncased`). Swap the checkpoint name to use a different model from the Hub.

## Inferencing With the Pipeline Class

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-10.jpg"/>
</p>

> Fill mask pipeline: `pipeline('fill-mask')` with `bert-base-uncased` predicts the word hidden by `[MASK]` in "I have to wake up in the morning and [MASK] a doctor" and prints each candidate word with its score.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-11.jpg"/>
</p>

> Sentiment analysis pipeline: given only the task name, the pipeline downloads a default model, tokenizes the text, runs the model, and returns a label with a score for "This is a great movie!" in about 3 lines of code.

## Inside the Pipeline: Model Inputs and Outputs

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-12.jpg"/>
</p>

> Full model: the model input goes through the transformer network (embeddings, then layers), which outputs hidden states. The head turns the hidden states into the final model output.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-13.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-14.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-15.jpg"/>
</p>

> Preparing the inputs: the tokenizer comes from the `distilbert-base-uncased-finetuned-sst-2-english` checkpoint. Two sentences are tokenized together with `padding=True` and `truncation=True`, and `return_tensors="pt"` returns PyTorch tensors. In the output, each row of `input_ids` starts with 101 ([CLS]). The shorter second sentence is padded with 0s, and its `attention_mask` uses 0 to tell the model to ignore those padding tokens.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-16.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-17.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-18.jpg"/>
</p>

> Post processing: the model outputs raw logits, which are not probabilities. `softmax` with `dim=-1` turns each row into probabilities that add up to 1. `model.config.id2label` maps index 0 to NEGATIVE and 1 to POSITIVE, so the first sentence is 96% positive and the second is 99.95% negative.

## Model Configuration, Loading, and Saving

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-19.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-20.jpg"/>
</p>

> Building a model from a config: `BertModel(BertConfig())` creates the BERT architecture with random weights, so it is useless for predictions until trained. The config holds attributes like `hidden_size` 768, `num_attention_heads` 12, and `num_hidden_layers` 12.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-21.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-22.jpg"/>
</p>

> Loading and saving: `from_pretrained("bert-base-cased")` loads the checkpoint trained by BERT's authors, ready for inference or fine tuning. `save_pretrained()` writes the config (`config.json`) and the weights file to a folder so the model can be reloaded later.

## Fine Tuning With the Trainer Class

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-23.jpg"/>
</p>

> Trainer: it takes the model, hyperparameters, metrics, training, validation, and test datasets, tokenizer, and data collator, and handles training, evaluation, and prediction without writing a training loop by hand.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-24.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-25.jpg"/>
</p>

> TrainingArguments: defines every training setting, including the output directory, number of epochs, batch sizes, learning rate, warmup steps, weight decay, logging, how often to evaluate and save, and whether to load the best model at the end. The example trains for 3 epochs with a learning rate of 5e-5 and mixed precision (`fp16=True`). Note: in recent versions of `transformers`, the `evaluation_strategy` argument shown in the screenshot is renamed `eval_strategy`.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-26.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-27.jpg"/>
</p>

> Creating and running the Trainer: pass the model, training arguments, tokenized training and validation datasets, data collator, and tokenizer, then call `trainer.train()` to fine tune. Note: in recent versions of `transformers`, the `tokenizer=` argument shown in the screenshot is renamed `processing_class=`.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-28.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-29.jpg"/>
</p>

> Computing metrics: `compute_metrics` receives an EvalPrediction (logits and labels), converts the logits to predicted classes with `np.argmax`, and scores them with the accuracy metric loaded from `evaluate`. Pass it to the Trainer with `compute_metrics=compute_metrics`.

## Vision Transformers (ViT)

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-32.jpg"/>
</p>

> Vision Transformer architecture: ViT is an encoder only model. The image is treated like a sentence and its patches like tokens. Instead of a decoder, the encoder's output for the class token goes straight into a feed forward network (the MLP head) to produce the classification output.

<br>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-30.jpg"/>
</p>

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/3-31.jpg"/>
</p>

> Image patching and embedding: the model's `image_processor` (ViT's version of a tokenizer) resizes and normalizes each image to match what the pretrained model expects. The image is split into patches, and the first layer linearly projects each flattened patch into a 768 value embedding. For `google/vit-base-patch16-224`, a 224 x 224 image becomes 196 patches of 16 x 16 pixels, and the learnable class token in front makes it 197 tokens. Self attention then scores how related every pair of patches is (a dog's nose patch scores high with its eye or ear patches), which gives ViT global context instead of a CNN's local receptive field. The class token's final vector goes through the classifier and softmax to produce class probabilities.
