import serial
import csv
from datetime import datetime

PORT = 'COM4'  # Replace with your actual COM port
BAUD = 115200

ser = serial.Serial(PORT, BAUD)
with open('wifi_log.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'SSID', 'RSSI'])
    while True:
        line = ser.readline().decode('utf-8').strip()
        if 'SSID:' in line:
            try:
                ssid = line.split('SSID: ')[1].split(',')[0]
                rssi = int(line.split('RSSI: ')[1])
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([ts, ssid, rssi])
                print(f"[{ts}] {ssid}: {rssi} dBm")
            except Exception as e:
                print("Error parsing:", line)
