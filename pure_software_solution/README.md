# AdMute - Pure Software Edition

This folder contains the complete source code for the "Pure Software" AdMute architecture. 

## How It Works
Instead of routing your TV's audio through a complex "Man-in-the-Middle" hardware chain, this solution treats the Raspberry Pi as a smart observer on your network.
1. **The Sensor**: A standard USB microphone on the Raspberry Pi listens to the ambient audio from your TV.
2. **The ML Model**: The audio stream is broken down into 0.96-second chunks and fed into a locally-running TensorFlow Lite model (Google's YAMNet).
3. **The Controller**: If a commercial is detected, the Pi utilizes the `pyatv` library to send native Apple TV commands over Wi-Fi, immediately setting the volume to zero. When the commercial concludes, it restores the volume.

## Getting Started
Head over to the [Installation Guide](docs/INSTALL.md) to learn how to:
1. Boot and SSH into your Raspberry Pi.
2. Install the necessary Python packages (`pyatv`, `pyaudio`, `tflite-runtime`).
3. Pair the AdMute software with your Apple TV.
