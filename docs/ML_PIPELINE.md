# AdMute Machine Learning Pipeline

This document details the machine learning process from data curation to on-device inference for classifying TV audio as "Commercial" or "Programming".

## 1. Problem Definition
The goal is a binary classification task on an audio stream:
- **Class 0**: Regular TV Programming (Movies, Shows, Sports)
- **Class 1**: Commercials (Advertisements)

Commercials typically have different audio signatures: dynamic range compression (they sound "louder"), specific fast-paced jingles, voice-overs, and different frequency distributions.

## 2. Model Architecture
For a Raspberry Pi to run real-time inference on an audio stream, the model must be lightweight.
- **Base Architecture**: MobileNetV2 or YamNet (which is based on MobileNetV1). YamNet is pre-trained on AudioSet and is excellent for audio classification.
- **Input**: Log-Mel Spectrogram (image representation of audio frequencies over time).
- **Output**: Softmax or Sigmoid probability of "Commercial".

## 3. Data Curation (`ml/curate_data.py`)
Since there isn't a perfect, up-to-date public dataset of *just* Apple TV commercials vs shows, we will build a custom dataset.
1. **Source**: YouTube videos of "TV commercial breaks 2023/2024" and "Full TV episodes".
2. **Extraction**: Use `yt-dlp` to download the audio tracks (`.wav` format, 16kHz mono).
3. **Chunking**: Split the audio into 1-second or 3-second overlapping chunks.
4. **Labeling**: Store chunks in folders `dataset/commercials/` and `dataset/shows/`.
5. **Preprocessing**: Convert the `.wav` chunks into Log-Mel Spectrograms to feed into the CNN.

## 4. Model Training (`ml/train.py`)
Using TensorFlow/Keras or PyTorch:
1. Load the preprocessed spectrograms.
2. Split into Train (80%), Validation (10%), and Test (10%) sets.
3. Apply Transfer Learning: Use YamNet/MobileNet as a feature extractor, replace the final classification head with a dense layer for our 2 classes.
4. Train with Early Stopping to prevent overfitting.
5. Save the final model as an `h5` or `SavedModel` format.

## 5. Quantization (`ml/quantize.py`)
To ensure the model runs instantly on the Pi without lag:
1. Use TensorFlow Lite Converter (`tf.lite.TFLiteConverter`).
2. Apply INT8 Post-Training Quantization (reduces model size from ~15MB to ~3MB).
3. Export `admute_model.tflite`.

## 6. On-Device Inference (`device/ml_engine.py`)
The Pi runs a loop:
1. Reads 1 second of audio from PulseAudio loopback.
2. Converts raw audio to Mel-Spectrogram using `librosa` or `tf.signal`.
3. Passes the spectrogram into the TFLite Interpreter.
4. If output probability > 0.85, trigger Mute. Otherwise, keep Unmuted.
