# AdMute MVP

AdMute is a proof-of-concept device built to automatically detect and mute television commercials in real-time. 

## Architectures

We have explored two distinct ways to build this:

### 1. Pure Software Solution (Recommended)
This is a lightweight, Wi-Fi-based architecture. A Raspberry Pi listens to the room using a standard USB microphone and runs a machine learning model to detect commercials. When an ad is detected, it connects to your Apple TV over your local Wi-Fi and sends a native volume control command to silence the output.
* **Pros**: No complex hardware, no audio lag, explicitly state-aware muting.
* **Code & Docs**: See the [`pure_software_solution/`](pure_software_solution/) directory.

### 2. Dual-Bluetooth Hardware Setup (Legacy)
Our original hardware PoC. The Raspberry Pi intercepts the digital audio stream acting as a Bluetooth receiver for the TV and a Bluetooth transmitter to the speaker, using a physical breadboard for hardware muting control.
* **Code & Docs**: See the [`dual_bluetooth_legacy/`](dual_bluetooth_legacy/) directory.
