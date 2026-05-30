# AdMute Installation & Setup Guide

This guide covers the setup of the Raspberry Pi hardware, OS configuration, and software installation required for the AdMute MVP using the Dual-Bluetooth architecture.

## 0. Initializing & Connecting to the Raspberry Pi
Before you can run the AdMute code, you need an operating system on the Raspberry Pi and a way to log into it.

1. **Flash OS**: Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your Mac. Insert your MicroSD card and use the Imager to flash **Raspberry Pi OS (64-bit)**. 
   - *Pro Tip*: Before clicking "Write", click the gear icon (Advanced Options) in the Imager. Check "Enable SSH", set a username/password (e.g., `pi` / `raspberry`), and configure your Wi-Fi credentials. This allows a "headless" setup!
2. **Boot the Pi**: Insert the SD card into the Raspberry Pi, plug in the USB-C power supply, and wait 2-3 minutes for it to boot and connect to Wi-Fi.
3. **Log In (SSH)**: On your Mac, open the Terminal and run:
   ```bash
   ssh pi@raspberrypi.local
   ```
   *(If you changed the username, replace `pi` with your username. If this doesn't work, you can plug a monitor and keyboard directly into the Pi instead).*

## 1. Hardware Assembly
1. **Add Second Bluetooth Radio**: Plug the USB Bluetooth Dongle into one of the USB ports on the Raspberry Pi.
2. **Wire the Breadboard**:
   - **ML Detection LED**: Connect the long leg to GPIO 18, and the short leg through a 330-ohm resistor to Ground (GND).
   - **Auto-Mute Status LED**: Connect the long leg to GPIO 22, and the short leg through a resistor to Ground (GND).
   - **Test Mute Button**: Connect one leg to GPIO 17, the other to Ground (GND).
   - **Auto-Mute Toggle Button**: Connect one leg to GPIO 27, the other to Ground (GND).

## 2. OS Installation & Configuration
1. **System Update**: Once logged into the Raspberry Pi terminal, run:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## 3. Dual-Bluetooth Setup
We need to configure the Pi to accept a connection from the Apple TV on the built-in radio (`hci0`), and connect to the HydraMotion on the USB dongle (`hci1`).

1. **Install PulseAudio and Bluetooth modules**:
   ```bash
   sudo apt install pulseaudio pulseaudio-module-bluetooth bluez-tools
   ```
2. **Configure PulseAudio for Loopback**:
   We will create a virtual loopback so incoming audio on `hci0` is routed to the output of `hci1`.
   ```bash
   # Add to ~/.config/pulse/default.pa
   load-module module-loopback latency_msec=10
   ```
3. **Pair the Devices**:
   Use `bluetoothctl` to pair the devices to their respective adapters.
   - **Apple TV**: Pair to the Pi's built-in adapter.
   - **HydraMotion**: Use `bluetoothctl -a hci1` to scan and pair the Pi to the Altec Lansing HydraMotion speaker.

## 4. Software Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/whs2k/sanity.git
   cd sanity
   ```
2. **Install Python Dependencies**:
   ```bash
   sudo apt install python3-pip python3-pyaudio
   pip3 install -r device/requirements.txt
   ```
3. **Run the Device Application**:
   ```bash
   python3 device/main.py
   ```

## 5. Machine Learning Setup (macOS / Local Training)
If you wish to re-train or generate the ML models on a Mac (especially Apple Silicon where pip dependencies like `numba` can fail), follow these steps:
1. **Install Miniconda**:
   ```bash
   brew install --cask miniconda
   ```
2. **Create the Conda Environment**:
   ```bash
   conda create -n admute python=3.11 -y
   conda activate admute
   ```
3. **Install ML Dependencies via Conda**:
   ```bash
   conda install -c conda-forge librosa pydub yt-dlp tensorflow tensorflow-hub numpy scikit-learn -y
   ```
4. **Run the Pipeline**:
   ```bash
   python ml/curate_data.py --url "<commercial_url>" --label commercial
   python ml/curate_data.py --url "<show_url>" --label show
   python ml/train.py
   python ml/quantize.py
   ```
