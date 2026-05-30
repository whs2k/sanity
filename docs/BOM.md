# AdMute Bill of Materials (BOM)

This document outlines the hardware components required to build the AdMute MVP device, utilizing a Dual-Bluetooth architecture.

## Core Hardware
| Component | Description | Estimated Cost | Example Link |
| :--- | :--- | :--- | :--- |
| **Raspberry Pi 4 (2GB or 4GB)** | The main computing unit that will run the OS, handle Bluetooth routing, and run the ML inference. | $45.00 - $55.00 | [Adafruit](https://www.adafruit.com/product/4292) |
| **Raspberry Pi Power Supply** | Official 15W USB-C power supply for the Raspberry Pi. | $8.00 | [Adafruit](https://www.adafruit.com/product/4298) |
| **MicroSD Card (32GB+)** | Fast storage for the Raspberry Pi OS, ML models, and audio caching. SanDisk Extreme or Samsung EVO recommended. | $10.00 | [Amazon](https://www.amazon.com/dp/B09B1GXM16) |

## Audio Routing & Connectivity
| Component | Description | Estimated Cost | Example Link |
| :--- | :--- | :--- | :--- |
| **USB Bluetooth 4.0/5.0 Dongle** | Adds a second Bluetooth radio to the Pi. One radio will receive from the Apple TV, the other will transmit to the HydraMotion. This dual setup prevents bandwidth congestion and lag. | $12.00 | [Amazon](https://www.amazon.com/dp/B0775YF36R) |

## Prototyping & Control
| Component | Description | Estimated Cost | Example Link |
| :--- | :--- | :--- | :--- |
| **Breadboard & Jumper Wires** | For prototyping the button and LED connections. | $10.00 | [Amazon](https://www.amazon.com/dp/B01EV70C78) |
| **Push Button (Momentary)** | To manually toggle the muting/auto-muting features. | $2.00 | [Adafruit](https://www.adafruit.com/product/1009) |
| **LED (Red/Green) & Resistors** | To signal when a commercial is detected. Includes a 330 ohm resistor. | $3.00 | [Adafruit](https://www.adafruit.com/product/299) |

**Estimated Total MVP Cost**: ~$90.00 USD
