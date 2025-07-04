import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

plt.style.use('seaborn-v0_8-darkgrid')  # 👈 Seaborn theme

# === Load and clean data ===
with open('wifi_log.csv', 'r', encoding='utf-8', errors='ignore') as f:
    df = pd.read_csv(f)

df = df[pd.to_numeric(df['RSSI'], errors='coerce').notnull()]
df['RSSI'] = df['RSSI'].astype(int)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df = df.dropna(subset=['Timestamp'])

# === Plot ===
fig, ax = plt.subplots(figsize=(14, 7))
colors = plt.cm.tab10.colors
for i, ssid in enumerate(df['SSID'].unique()):
    data = df[df['SSID'] == ssid]
    ax.plot(data['Timestamp'], data['RSSI'], marker='o', label=ssid, color=colors[i % len(colors)])

ax.axhline(y=-75, color='red', linestyle='--', linewidth=1.2, label='Weak Signal Threshold')
ax.set_title('📶 Wi-Fi Signal Strength Over Time', fontsize=16, weight='bold')
ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('RSSI (dBm)', fontsize=12)
ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
plt.xticks(rotation=45)
ax.legend(title='SSID', loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig('rssi_plot.png')
plt.show()
