pip install yfinance
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.signal import find_peaks

# Download data
ticker = "BBRI.JK"
start_date = "2020-01-01"
end_date = "2026-08-01"

data = yf.download(ticker, start=start_date, end=end_date, progress=False)

close = data['Close'].values
close_ser = data['Close'].dropna()
close_flat = np.asarray(close_ser.values).flatten()
N = len(close)
print(f"Download {N} close {ticker} {start_date} - {end_date}")

# detrend
close_mean = np.mean(close)
signal = close - close_mean

# FFT
fft_vals = np.fft.fft(signal)
fft_freqs = np.fft.fftfreq(N, d=1)  

# Identifikasi peak dominan / frekuensi non-zero
mag = np.abs(fft_vals)
# reduksi freq 0
mag[0] = 0

peak_idx = np.argmax(mag)
peak_freq = fft_freqs[peak_idx]
peak_mag = mag[peak_idx] 
print(f"Frekuensi Puncak: {peak_freq:.6f} siklus/hari (magnitude {peak_mag[0]:.2f})")

# Konversi ke periode
if peak_freq != 0:
    cycle_period = 1.0 / abs(peak_freq)
    print(f"Estimasi siklus periode dominan : {cycle_period:.2f} hari")
else:
    cycle_period = None
    print("Tidak ada frekuensi puncak.")

# Deteksi Peak Through
window = cycle_period/2
peaks, _ = find_peaks(close_flat, distance=window)
troughs, _ = find_peaks(-close_flat, distance=window)

print(f"Terdapat {len(peaks)} peak dan {len(troughs)} trough.")

peak_dates = close_ser.index[peaks]
trough_dates = close_ser.index[troughs]

peak_intervals = np.diff(peak_dates) / np.timedelta64(1, 'D')
trough_intervals = np.diff(trough_dates) / np.timedelta64(1, 'D')

avg_peak_cycle = np.mean(peak_intervals) if len(peak_intervals) > 0 else None
avg_trough_cycle = np.mean(trough_intervals) if len(trough_intervals) > 0 else None

print("\nHasil Deteksi Puncak:")
if avg_peak_cycle:
    print(f"Rata-rata interval peak-to-peak : {avg_peak_cycle:.2f} hari")
if avg_trough_cycle:
    print(f"Rata-rata interval trough-to-trough : {avg_trough_cycle:.2f} hari")

# Plot
plt.figure(figsize=(12, 10)) 

ax1 = plt.subplot(4, 1, 1)
ax1.plot(data.index, close, label='Harga Close')
ax1.set_title(f"{ticker} Harga Close")
ax1.set_ylabel("Harga")
ax1.grid(True)
ax1.legend()

ax1b = plt.subplot(4, 1, 2, sharex=ax1)
ax1b.plot(data.index, signal, '--', color='orange', label='Detrended')
ax1b.set_title(f"{ticker} Harga Detrended")
ax1b.set_ylabel("Harga Detrended")
ax1b.grid(True)
ax1b.legend()


ax2 = plt.subplot(4, 1, 3)
ax2.plot(fft_freqs, mag, linewidth=1)
ax2.set_title("Spektrum FFT")
ax2.set_xlabel("Frekuensi (siklus/hari)")
ax2.set_ylabel("Magnitud")
ax2.grid(True)

# Marker Peak dan Through
ax2.axvline(peak_freq, color='red', linestyle='--')
ax2.axvline(-peak_freq, color='red', linestyle='--')
ax2.annotate(f"{cycle_period:.1f} h",
              xy=(peak_freq, peak_mag),
              xytext=(peak_freq, peak_mag * 0.5),
              arrowprops=dict(arrowstyle="->", color="red"))

ax3 = plt.subplot(4, 1, 4, sharex=ax1) 
ax3.plot(close_ser.index, close, label='Close')
ax3.plot(peak_dates, close[peaks], "x", label="Peaks")
ax3.plot(trough_dates, close[troughs], "+", label="Troughs")
ax3.set_title("Harga Closing dengan Peaks/Troughs")
ax3.grid(True)
ax3.legend()


plt.tight_layout()
plt.show()
