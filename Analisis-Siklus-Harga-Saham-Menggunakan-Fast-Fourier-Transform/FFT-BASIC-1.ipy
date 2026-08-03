import numpy as np
import matplotlib.pyplot as plt

# parameter
days = 365          
period = 30         
amplitude = 10      
noise_level = 2     

# time series 
t = np.arange(days)
signal = amplitude * np.sin(2 * np.pi * t / period)   # sinus dengan siklus 30 hari
signal += noise_level * np.random.randn(days)         # Noise Gaussian

# FFT
fft_vals = np.fft.fft(signal)
fft_freqs = np.fft.fftfreq(len(signal), d=1)   # siklus/hari

# Frekuensi Puncak 
positive_freq_mask = fft_freqs > 0
peak_frequency_index = np.argmax(np.abs(fft_vals[positive_freq_mask]))
peak_frequency = fft_freqs[positive_freq_mask][peak_frequency_index]
peak_amplitude = np.abs(fft_vals[positive_freq_mask][peak_frequency_index])

# Periode dari frekuensi puncak
peak_period = 1 / peak_frequency

# plot
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot signal
axs[0].plot(t, signal)
axs[0].set_title("Signal Time Series")
axs[0].set_xlabel("Hari")
axs[0].set_ylabel("Amplitudo")
axs[0].grid(True)
axs[0].set_xticks(np.arange(0, days, 15))


# Plot FFT
axs[1].plot(fft_freqs, np.abs(fft_vals), linewidth=1)
axs[1].set_title("FFT dari Time Series dengan siklus 30-Day")
axs[1].set_xlabel("Freqkuensi (siklus/hari)")
axs[1].set_ylabel("Amplitudo")
axs[1].grid(True)

axs[1].plot(peak_frequency, peak_amplitude, 'ro')  
axs[1].annotate(f'Frekuensi Puncak: {peak_frequency:.3f} siklus/hari Periode Puncak: {peak_period:.2f} hari',
                 xy=(peak_frequency, peak_amplitude),
                 xytext=(peak_frequency + 0.01, peak_amplitude + 10),
                 arrowprops=dict(facecolor='black', shrink=0.05))


plt.tight_layout()
plt.show()
