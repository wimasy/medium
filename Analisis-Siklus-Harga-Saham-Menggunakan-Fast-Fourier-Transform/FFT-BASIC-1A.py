import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf

# parameters
days = 365          
periods = [30,45,60] 
amplitudes = [5,15,10]  
phases = [0, np.pi/4, np.pi/2] 
noise_level = 2     

# time series 
t = np.arange(days)
signal = np.zeros(days) 

# Generate signal
for period, amplitude, phase in zip(periods, amplitudes, phases):
    signal += amplitude * np.sin(2 * np.pi * t / period + phase)

signal += noise_level * np.random.randn(days)         # Noise Gaussian

# FFT
fft_vals = np.fft.fft(signal)
fft_freqs = np.fft.fftfreq(len(signal), d=1)  

# Frekuensi Puncak 
positive_freq_mask = fft_freqs > 0
positive_fft_freqs = fft_freqs[positive_freq_mask]
positive_fft_vals = np.abs(fft_vals[positive_freq_mask])

# cari N puncak dari jumlah periode
num_peaks = len(periods)
peak_indices = np.argsort(positive_fft_vals)[-num_peaks:][::-1]
peak_frequencies = positive_fft_freqs[peak_indices]
peak_amplitudes = positive_fft_vals[peak_indices]
peak_periods = 1 / peak_frequencies


# --- plot ---
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

axs[0].plot(t, signal)
axs[0].set_title("Signal Time Series dengan Multiple Periods")
axs[0].set_xlabel("Hari")
axs[0].set_ylabel("Amplitudo")
axs[0].grid(True)
axs[0].set_xticks(np.arange(0, days, 15)) # Set x-axis ticks every 15 days


# Plot FFT
axs[1].plot(fft_freqs, np.abs(fft_vals), linewidth=1)
axs[1].set_title("FFT Signal Time Series dengan Multiple Periods")
axs[1].set_xlabel("Frequency (siklus/hari)")
axs[1].set_ylabel("Amplitudo")
axs[1].grid(True)

for i in range(num_peaks):
    axs[1].plot(peak_frequencies[i], peak_amplitudes[i], 'ro')  
    axs[1].annotate(f'Frek: {peak_frequencies[i]:.3f} siklus/hari, Periode: {peak_periods[i]:.2f} hari',
                     xy=(peak_frequencies[i], peak_amplitudes[i]),
                     xytext=(peak_frequencies[i] + 0.01, peak_amplitudes[i] + 1 * (num_peaks - i)), 
                     arrowprops=dict(facecolor='black', arrowstyle='->,head_width=.15', linewidth=0.5)) 


plt.tight_layout() 
plt.show()
