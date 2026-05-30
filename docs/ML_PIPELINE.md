# AdMute Machine Learning Pipeline

This document details the machine learning process from data curation to on-device inference using Google's YAMNet.

## 1. Problem Definition
The goal is a binary classification task on an audio stream:
- **Class 0**: Regular TV Programming (Movies, Shows, Sports)
- **Class 1**: Commercials (Advertisements)

## 2. Model Architecture: YAMNet
We will use Google's **YAMNet**, a pre-trained deep net that predicts 521 audio event classes based on the AudioSet-YouTube corpus. It employs a MobileNetV1 architecture and takes audio waveforms as input, computing log-mel spectrograms internally.

Instead of training a model from scratch, we will **fine-tune** YAMNet or use it as a feature extractor.

## 3. Data Curation (`ml/curate_data.py`)
To adapt YAMNet to our specific Apple TV commercial vs. show problem, we will script the creation of a custom dataset.
1. **Source**: YouTube videos of "TV commercial breaks 2024" and "Full TV episodes".
2. **Extraction**: `yt-dlp` will download the audio tracks (`.wav` format, 16kHz mono).
3. **Chunking**: `librosa` or `pydub` will split the audio into 0.96-second chunks (the exact input size YAMNet expects).
4. **Labeling**: Store chunks in `dataset/commercials/` and `dataset/shows/`.

## 4. Model Training (`ml/train.py`)
1. **Load YAMNet**: Load the pre-trained YAMNet model from TensorFlow Hub.
2. **Feature Extraction**: Pass our chunked audio dataset through YAMNet to extract the 1024-dimensional embeddings (the layer right before the final classification).
3. **Classification Head**: Train a small, new Dense neural network layer on top of these embeddings to classify into our 2 classes.
4. **Export**: Save the combined model.

## 5. Quantization (`ml/quantize.py`)
To ensure the model runs instantly on the Pi without lag:
1. Use TensorFlow Lite Converter (`tf.lite.TFLiteConverter`).
2. Apply INT8 Post-Training Quantization.
3. Export `admute_yamnet.tflite`.

## 6. On-Device Inference (`device/main.py`)
The Pi runs a loop:
1. Reads 0.96 seconds of audio from the PulseAudio loopback.
2. Passes the waveform directly into the TFLite Interpreter.
3. If output probability > 0.85, mute the output Bluetooth sink. Otherwise, keep Unmuted.

## 7. Initial Training Results (MVP Model)
The initial MVP model (`admute_yamnet.tflite`) was trained using a custom curated dataset:
- **Commercial Data**: Avatar Movie Trailer (438 audio chunks).
- **Show Data**: Big Buck Bunny (1321 audio chunks).

**Results**:
- **Training Accuracy**: 98.8%
- **Validation Accuracy**: 96.0%
- **Original Model Size**: ~20.40 MB
- **Quantized TFLite Size**: 3.26 MB

This quantized model provides excellent baseline accuracy and is lightweight enough for real-time inference on the Raspberry Pi 4 without audio lag.
