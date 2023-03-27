Prerequisites:
- Connect ESP32 with computer using usb
- Ensure CP210x UART is installed
- Ensure Python is installed and esptool.py (e.g. using pip install esptool)
- Download stable version of Micropython .bin file for ESP32 (e.g. v1.18)
- Find serial port name in device manager (Windows) e.g. COM5
- Install Putty
- Download local webrepl

Install:
- Erase Flash: python -m esptool --chip esp32 erase_flash
- Install micropython bin: python -m esptool --chip esp32 --port COM5 write_flash -z 0x1000 esp32-20220117-v1.18.bin

Upload source files:
- Using Putty connect with COM port using baudrate 115200
import network
- Execute commands to setup access point and start webrepl:
ap = network.WLAN(network.AP_IF)
ap.active(True) 

import webrepl
webrepl.start()

- Connect computer to access point of esp32
- Open webrepl
- Connect with ws://192.168.4.1:8266/
- Select files and send to device
- 