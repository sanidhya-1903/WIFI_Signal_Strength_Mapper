import serial
import csv
from datetime import datetime
import statistics

# === CONFIGURATION ===
PORT = 'COM4'        # Replace with your correct COM port
BAUD = 115200
THRESHOLD_RSSI = -75
ALERT_COUNT = 3      # Alerts if RSSI is below threshold 3+ times

# === LOCATION TAG ===
location_tag = input("📍 Enter current location name (e.g., Lab, Hall): ")

# === START SERIAL ===
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"[INFO] Serial connected on {PORT}")
except Exception as e:
    print(f"[ERROR] Could not connect to {PORT}: {e}")
    exit()

# === TRACKING STRUCTURES ===
ssid_data = {}
low_signal_counter = {}

# === LOG FILE ===
logfile = "wifi_log.csv"
with open(logfile, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'SSID', 'RSSI', 'Location', 'Avg_RSSI', 'Std_Dev', 'Above_Threshold(%)'])

    print("[INFO] Logging started...\nPress Ctrl+C to stop.\n")

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()

            if 'SSID:' in line and 'RSSI:' in line:
                try:
                    ssid = line.split('SSID: ')[1].split(',')[0].strip()
                    rssi_str = line.split('RSSI: ')[1].strip().split()[0]  # Fixes "dBm (secured)" issue
                    rssi = int(rssi_str)
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


                    # Stats tracking
                    if ssid not in ssid_data:
                        ssid_data[ssid] = []
                        low_signal_counter[ssid] = 0

                    ssid_data[ssid].append(rssi)
                    if len(ssid_data[ssid]) > 50:
                        ssid_data[ssid].pop(0)

                    avg = round(statistics.mean(ssid_data[ssid]), 2)
                    std = round(statistics.stdev(ssid_data[ssid]), 2) if len(ssid_data[ssid]) > 1 else 0
                    above = sum(1 for x in ssid_data[ssid] if x > THRESHOLD_RSSI)
                    above_pct = round(100 * above / len(ssid_data[ssid]), 1)

                    # Alert system
                    if rssi < THRESHOLD_RSSI:
                        low_signal_counter[ssid] += 1
                    else:
                        low_signal_counter[ssid] = 0

                    if low_signal_counter[ssid] >= ALERT_COUNT:
                        print(f"⚠️  ALERT: {ssid} weak signal for {ALERT_COUNT}+ scans!")

                    # Log to CSV
                    writer.writerow([timestamp, ssid, rssi, location_tag, avg, std, above_pct])
                    file.flush()

                    # Print to terminal
                    print(f"[{timestamp}] {ssid}: {rssi} dBm | Avg: {avg} | Std: {std} | Above -75dBm: {above_pct}%")

                except Exception as e:
                    print(f"[WARN] Failed to parse line: {line} ({e})")

        except KeyboardInterrupt:
            print("\n[INFO] Logging stopped by user.")
            break
