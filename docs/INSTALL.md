# AdMute Installation & Setup Guide

This guide covers the setup of the Raspberry Pi hardware, OS configuration, and software installation required for the AdMute MVP.

## 1. Hardware Assembly
1. **Prepare the Pi**: Insert the SD card (flashed in Step 2) into the Raspberry Pi.
2. **Connect Audio**: Plug the 3.5mm Aux cable from the Raspberry Pi's audio jack to the Altec Lansing speaker.
3. **Wire the Breadboard**:
   - **LED**: Connect the long leg (anode) of the LED to GPIO Pin 18. Connect the short leg (cathode) through a 330-ohm resistor to a Ground (GND) pin.
   - **Button**: Connect one leg of the push button to GPIO Pin 17, and the other leg to a Ground (GND) pin. (We will use internal pull-up resistors in software).
4. **Power On**: Plug in the USB-C power supply.

## 2. OS Installation & Configuration
1. **Flash OS**: Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash **Raspberry Pi OS (64-bit)** to your MicroSD card.
2. **Initial Setup**: Boot the Pi, connect it to your Wi-Fi network, and enable SSH via `sudo raspi-config` > Interface Options > SSH.
3. **System Update**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## 3. Bluetooth Audio Receiver Setup
We need to configure the Pi to accept Bluetooth connections and route them to PulseAudio.
1. **Install PulseAudio and Bluetooth modules**:
   ```bash
   sudo apt install pulseaudio pulseaudio-module-bluetooth bluez-tools
   ```
2. **Enable PulseAudio Service**:
   ```bash
   systemctl --user enable pulseaudio
   systemctl --user start pulseaudio
   ```
3. **Configure Bluetooth to trust Apple TV**:
   Use `bluetoothctl` to make the Pi discoverable:
   ```bash
   bluetoothctl
   # Inside bluetoothctl prompt:
   discoverable on
   pairable on
   agent on
   default-agent
   ```
   *On your Apple TV, go to Settings > Remotes and Devices > Bluetooth, and select your Raspberry Pi to pair.*

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
