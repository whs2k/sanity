# AdMute - Pure Software Setup Guide

Follow these steps to deploy the Wi-Fi-based AdMute software onto a fresh Raspberry Pi.

## 1. Initializing & Connecting to the Raspberry Pi

1. **Flash OS**: Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your Mac. Insert your MicroSD card and use the Imager to flash **Raspberry Pi OS (64-bit)**. 
   - *Pro Tip*: Before clicking "Write", click the gear icon (Advanced Options) in the Imager. Check "Enable SSH", set a username/password (e.g., `pi` / `raspberry`), and configure your Wi-Fi credentials.
2. **Boot the Pi**: Insert the SD card, plug in the USB microphone, plug in power, and wait 2-3 minutes.
3. **Log In (SSH)**: On your Mac, open the Terminal and run:
   ```bash
   ssh pi@raspberrypi.local
   ```

## 2. Software Installation

Once logged into the Raspberry Pi terminal:

1. **System Update**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/whs2k/sanity.git
   cd sanity/pure_software_solution
   ```
3. **Install System Dependencies**:
   ```bash
   sudo apt install python3-pip python3-pyaudio python3-venv
   ```
4. **Install Python Packages**:
   It is highly recommended to use a virtual environment on the Pi.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r device/requirements.txt
   ```

## 3. Apple TV Pairing

Apple TVs require a security PIN pairing before 3rd party applications can control them. We will use the `atvremote` CLI tool (which comes with `pyatv`).

1. **Find your Apple TV**:
   ```bash
   atvremote scan
   ```
   *Note the IP address or identifier of your Apple TV.*
2. **Initiate Pairing**:
   ```bash
   atvremote -i <YOUR_APPLE_TV_IP> pair
   ```
3. **Enter the PIN**: Your TV screen will display a 4-digit PIN. Type this PIN into the Raspberry Pi terminal when prompted.

## 4. Run the Application

With the Apple TV paired and the microphone plugged in, start the device loop!

```bash
python device/main.py
```
