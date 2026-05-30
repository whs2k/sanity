# AdMute - Pure Software Setup Guide

Follow these steps to deploy the Wi-Fi-based AdMute software onto a fresh Raspberry Pi (including the Raspberry Pi Zero 2 W).

## 1. Initializing & Connecting to the Raspberry Pi

Because you are using a Raspberry Pi as a "headless" server (without plugging it into a monitor or keyboard), you will connect to it remotely from your Mac using a protocol called SSH (Secure Shell). Here is the exact physical flow:

1. **Download the Imager**: Go to [raspberrypi.com/software/](https://www.raspberrypi.com/software/) on your Mac and download the **Raspberry Pi Imager**.
2. **Configure the OS**: Insert your MicroSD card into your Mac. Open the Imager, choose **Raspberry Pi OS (64-bit)** (or 32-bit if using a very old Pi), and select your SD card.
3. **The "Headless" Secret (Crucial Step)**: Before clicking "Write", click the **Edit Settings** button (or gear icon) in the Imager. You must configure three things here:
   - Check **Enable SSH** (Use password authentication).
   - Set a **username and password** (e.g., username: `pi`, password: `raspberry`).
   - Check **Configure wireless LAN** and enter your exact home Wi-Fi name and password. This is what allows the Pi to automatically join your network when it turns on!
4. **Flash & Insert**: Click "Write". Once finished, take the SD card out of your Mac and insert it into the slot on your Raspberry Pi.
5. **Boot Up**: Plug the USB microphone and the power cable into the Raspberry Pi. Wait about 2 to 3 minutes. During this time, the Pi is booting up and silently connecting to your home Wi-Fi network using the credentials you provided in Step 3.
6. **Log In (SSH)**: Now, open the **Terminal** app on your Mac. Type the following command to securely connect to the Pi over your Wi-Fi network:
   ```bash
   ssh pi@raspberrypi.local
   ```
   *(If you used a username other than `pi` in step 3, replace `pi` with that username). It will ask for your password. When you type it, the characters won't show up on screen—just type it and press Enter! You are now remotely controlling the Raspberry Pi!*

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
