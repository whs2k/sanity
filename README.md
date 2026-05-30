# AdMute MVP

AdMute is a proof-of-concept device built to automatically detect and mute television commercials in real-time. It acts as a smart "Man-in-the-Middle" between your media player (e.g., Apple TV) and your Bluetooth speaker.

## 1. How It Works

AdMute uses a **Dual-Bluetooth Hardware Architecture** powered by a Raspberry Pi 4:
- **Receiver**: The Pi's built-in Bluetooth pairs with your Apple TV as an audio sink.
- **Transmitter**: A secondary USB Bluetooth dongle pairs with your speaker (e.g., Altec Lansing HydraMotion) as an audio source.
- **Audio Routing**: Linux `PulseAudio` creates a seamless internal loopback from the receiver directly to the transmitter.

While the audio flows through the Pi, a background Python process continuously captures 0.96-second audio chunks using `PyAudio`. These chunks are passed into a highly optimized, quantized **Google YAMNet** machine learning model (`admute_yamnet.tflite`). The neural network classifies the audio in real-time. When it detects a commercial with high confidence (>80%), it issues a system command to instantly mute the outgoing Bluetooth speaker connection. When the commercial ends, it unmutes the stream.

## 2. Installation & Setup

### Hardware Requirements
- Raspberry Pi 4 (Running Raspberry Pi OS / Debian)
- USB Bluetooth Dongle (for the secondary transmitter)
- Physical Push Button (wired to GPIO 17)
- LED Indicator (wired to GPIO 18)

### Software Setup
1. **PulseAudio Configuration**:
   Follow the detailed guide in `docs/INSTALL.md` to configure the dual-Bluetooth PulseAudio loopback.
2. **Clone and Install**:
   ```bash
   git clone https://github.com/whs2k/sanity.git
   cd sanity
   sudo apt update
   sudo apt install python3-pip python3-pyaudio
   pip3 install -r device/requirements.txt
   ```
3. *(Optional) Machine Learning Retraining*:
   If you wish to retrain the model on macOS or Linux, see the local setup instructions in `docs/INSTALL.md` and the pipeline overview in `docs/ML_PIPELINE.md`.

## 3. Functionality

Once deployed and running on the Raspberry Pi (`python3 device/main.py`), the following features are active:

- **End-to-End Auto-Muting**: The background Machine Learning loop runs continuously. As soon as it identifies a commercial in the incoming audio stream, it mutes the Bluetooth speaker automatically.
- **Visual Feedback**: The physical LED on the device instantly illuminates whenever a commercial is detected and the audio is muted, providing clear status verification.
- **Manual Override**: The physical push button on the device triggers hardware interrupts. Pressing the button allows you to instantly toggle the muting state manually at any time.
