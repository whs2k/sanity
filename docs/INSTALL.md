# AdMute Installation & Setup Guide

This guide covers the setup of the Raspberry Pi hardware, OS configuration, and software installation required for the AdMute MVP using the Dual-Bluetooth architecture.

## 1. Hardware Assembly
1. **Prepare the Pi**: Insert the SD card into the Raspberry Pi.
2. **Add Second Bluetooth Radio**: Plug the USB Bluetooth Dongle into one of the USB ports on the Raspberry Pi.
3. **Wire the Breadboard**:
   - **LED**: Connect the long leg (anode) of the LED to GPIO Pin 18. Connect the short leg (cathode) through a 330-ohm resistor to a Ground (GND) pin.
   - **Button**: Connect one leg of the push button to GPIO Pin 17, and the other leg to a Ground (GND) pin.
4. **Power On**: Plug in the USB-C power supply.

## 2. OS Installation & Configuration
1. **Flash OS**: Use the Raspberry Pi Imager to flash **Raspberry Pi OS (64-bit)**.
2. **System Update**:
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
