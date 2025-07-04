# Wi-Fi Signal Strength Mapper

This project logs and visualizes Wi-Fi signal strength using an **ESP8266 (NodeMCU)** and **Python**. It continuously scans available networks, logs RSSI values with timestamps, and generates a graph showing signal strength trends over time.

## Features
- Real-time RSSI scanning via ESP8266
- CSV logging of SSID, RSSI, and timestamp
- Auto-generated RSSI graph
- Weak signal alert line at -75 dBm
- Optional: Plotly for interactive graphs

## Components Used
- ESP8266 (NodeMCU)
- Python 3.x
- Libraries: `pyserial`, `pandas`, `matplotlib`

## How to Use

### Upload to ESP8266
- Open `esp8266_code/wifi_scanner.ino` in Arduino IDE
- Select `NodeMCU 1.0 (ESP-12E)` board
- Upload to device

### Run Python Logger
Update the COM port in `logger.py`:
```python
PORT = 'COMX'  # Change based on Device Manager
