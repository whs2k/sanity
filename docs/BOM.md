# AdMute Bill of Materials (BOM)

This document outlines the hardware components required to build the AdMute MVP device. 

## Core Hardware
| Component | Description | Estimated Cost | Example Link |
| :--- | :--- | :--- | :--- |
| **Raspberry Pi 4 (2GB or 4GB)** | The main computing unit that will run the OS, handle Bluetooth routing, and run the ML inference. | $45.00 - $55.00 | [Adafruit](https://www.adafruit.com/product/4292) |
| **Raspberry Pi Power Supply** | Official 15W USB-C power supply for the Raspberry Pi. | $8.00 | [Adafruit](https://www.adafruit.com/product/4298) |
| **MicroSD Card (32GB+)** | Fast storage for the Raspberry Pi OS, ML models, and audio caching. SanDisk Extreme or Samsung EVO recommended. | $10.00 | [Amazon](https://www.amazon.com/dp/B09B1GXM16) |

## Audio Routing & Connectivity
| Component | Description | Estimated Cost | Example Link |
| :--- | :--- | :--- | :--- |
| **3.5mm Aux Audio Cable** | To connect the Raspberry Pi's audio output to the Altec Lansing speaker. | $5.00 | [Amazon](https://www.amazon.com/dp/B00NO73MUQ) |

## Prototyping & Control
| Component | Description | Estimated Cost | Example Link |
| :--- | :--- | :--- | :--- |
| **Breadboard & Jumper Wires** | For prototyping the button and LED connections. | $10.00 | [Amazon](https://www.amazon.com/dp/B01EV70C78) |
| **Push Button (Momentary)** | To manually toggle the muting/auto-muting features. | $2.00 | [Adafruit](https://www.adafruit.com/product/1009) |
| **LED (Red/Green) & Resistors** | To signal when a commercial is detected. Includes a 330 ohm resistor. | $3.00 | [Adafruit](https://www.adafruit.com/product/299) |

## Optional (But Recommended)
| Component | Description | Estimated Cost | Example Link |
| :--- | :--- | :--- | :--- |
| **USB Sound Card** | The Pi's built in 3.5mm audio can sometimes be noisy. A cheap USB to 3.5mm adapter improves audio quality. | $8.00 | [Amazon](https://www.amazon.com/dp/B00IRVQ0F8) |

**Estimated Total MVP Cost**: ~$91.00 USD
