pip install yfinance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm

# Data Saham 
ticker = "BMRI.JK"
start = "2025-06-01"
end = "2026-06-01"
data = yf.download(ticker, start, end)

# Log Return Harian
data['Return'] = np.log(data['Close'] / data['Close'].shift(1))
returns = data['Return'].dropna()

# Mean dan standard deviation
mu, sigma = returns.mean(), returns.std()

fig, axes = plt.subplots(3, 1, figsize=(10, 12))

# Histogram Frekuensi Log Return
axes[0].hist(returns, bins=100, color='skyblue', edgecolor='black')
axes[0].set_title(f'{ticker} Daily Log Returns (Frequency)')
axes[0].set_xlabel('Daily Return')
axes[0].set_ylabel('Number of Days')
axes[0].grid(True)

# Histogram Probability Density Histogram + Kurva Normal
axes[1].hist(returns, bins=100, density=True, color='skyblue', edgecolor='black', alpha=0.6)
x = np.linspace(returns.min(), returns.max(), 1000)
pdf = norm.pdf(x, mu, sigma)
axes[1].plot(x, pdf, color='red', linewidth=2, label=f'Normal Fit (μ={mu:.4f}, σ={sigma:.4f})')
axes[1].set_title(f'{ticker} Daily Log Returns (Probability Density)')
axes[1].set_xlabel('Daily Return')
axes[1].set_ylabel('Probability Density')
axes[1].legend()
axes[1].grid(True)

# Cumulative Distribution Function
cdf = norm.cdf(x, mu, sigma)
axes[2].plot(x, cdf, color='green', linewidth=2)
axes[2].set_title(f'{ticker} Daily Log Return CDF')
axes[2].set_xlabel('Daily Return')
axes[2].set_ylabel('Cumulative Probability')
axes[2].grid(True)

plt.tight_layout()
plt.show()

# Peluang untuk positif +1% 
p_gain = 1 - norm.cdf(0, mu, sigma)
p_gain_1 = 1 - norm.cdf(0.01, mu, sigma)
p_gain_2 = 1 - norm.cdf(0.02, mu, sigma)
p_gain_3 = 1 - norm.cdf(0.03, mu, sigma)

p_gain_0_1 = norm.cdf(0.01, mu, sigma) - norm.cdf(0.00, mu, sigma)
p_loss_0_1 = norm.cdf(-0.01, mu, sigma) - norm.cdf(0.00, mu, sigma)

# Peluang untuk rugi lebih dari -1%
p_loss = norm.cdf(0, mu, sigma)
p_loss_1 = norm.cdf(-0.01, mu, sigma)
p_loss_2 = norm.cdf(-0.02, mu, sigma)
p_loss_3 = norm.cdf(-0.03, mu, sigma)

p_gain_0_2 = norm.cdf(0.02, mu, sigma) - norm.cdf(0.01, mu, sigma)
p_loss_0_2 = norm.cdf(-0.01, mu, sigma) - norm.cdf(-0.02, mu, sigma)

expected_freq_2 = round(1/p_gain_0_2)
expected_freq_2_loss = round(1/p_loss_0_2)

print(f"Jumlah hari trading {len(data)} hari")
print(f"Rata-rata return harian mu: {mu:.5f}")
print(f"Standar deviasi sigma: {sigma:.5f}")

print(f"Peluang gain : {p_gain*100:.2f}%")
print(f"Peluang gain >1%: {p_gain_1*100:.2f}%")
print(f"Peluang gain >2%: {p_gain_2*100:.2f}%")
print(f"Peluang gain >3%: {p_gain_3*100:.2f}%")

print(f"Peluang loss < 0%: {p_loss*100:.2f}%")
print(f"Peluang loss <-1%: {p_loss_1*100:.2f}%")
print(f"Peluang loss <-2%: {p_loss_2*100:.2f}%")
print(f"Peluang loss <-3%: {p_loss_3*100:.2f}%")

print(f"Peluang gain +1%< x < +2%: {p_gain_0_2*100:.2f}%")
print(f"Peluang loss -2% < x < -1%: {p_loss_0_2*100:.2f}%")

print(f"Frekuensi harapan gain 0< x < +2%: setiap {expected_freq_2:.1f} hari trading")
print(f"Frekuensi harapan loss 0< x < -2%: setiap {expected_freq_2_loss:.1f} hari trading")
print(f"Dalam {len(data)} hari trading Frekuensi harapan gain 0< x < 1%: setiap {len(data)*p_gain_0_1:.2f} hari" )
print(f"Peluang gain 0% < X < 2% {p_gain_0_2*100:.2f}%")

ranges = [
    (-0.02, -0.01),  # -2% to -1%
    (-0.01, 0.00),   # -1% to 0%
    (0.00, 0.01),    # 0% to +1%
    (0.01, 0.02),    # +1% to +2%
    (0.02, 0.03),    # +2% to +3%
]

# Probabilitas dan frekuensi harapan masing-masing rentang gain/loss
print(f"\nTicker: {ticker}", start,"-",end)
print(f"Mean (μ): {mu:.5f}, Std (σ): {sigma:.5f}")
print("\nRentang (%)\t\tPeluang\t\tFrek. Harapan (hari)\n" + "-"*45)

for lower, upper in ranges:
    p = norm.cdf(upper, mu, sigma) - norm.cdf(lower, mu, sigma)
    freq = 1 / p if p > 0 else np.inf
    print(f"{lower*100:>5.1f}% to {upper*100:<4.1f}%\t{p:>8.3%}\t\t{freq:>8.2f}")

# Kejadian ekstrim 
p_extreme_high = 1 - norm.cdf(0.03, mu, sigma)
p_extreme_low = norm.cdf(-0.02, mu, sigma)
print("\nKejadian Ekstrem: (gain > +3% loss < -2%)")
print(f"rₜ > +3%: {p_extreme_high:.3%} (≈ 1 dalam {1/p_extreme_high:.1f} hari)")
print(f"rₜ < -2%: {p_extreme_low:.3%} (≈ 1 dalam {1/p_extreme_low:.1f} hari)")
