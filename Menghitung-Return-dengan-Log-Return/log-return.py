import math
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

tickers = ['BMRI.JK', 'BBRI.JK', 'BBNI.JK', 'BRIS.JK', 'BBCA.JK']
start_date = "2020-01-01"
end_date = "2025-12-31"

years=5

data = yf.download(tickers, start=start_date, end=end_date, interval='1d', auto_adjust=True)['Close']
data = data.dropna()

year_end_prices = data.groupby(data.index.year).last().tail(years)
year_end_prices.index = [f"p{i}" for i in range(years)]

price_df = year_end_prices.T.copy()

portfolio_sum = price_df.sum()
price_df.loc['Portfolio Total'] = portfolio_sum

weights = pd.DataFrame(index=tickers)
for i in range(len(portfolio_sum)):
    period = f"p{i}" 
    total = portfolio_sum[period]
    weights[period] = price_df.loc[tickers, period] / total

weights = weights.T
weights.index.name = 'Period'

# Log Return
log_data = []
for stock in tickers:
    prices = price_df.loc[stock].values
    log_returns = [math.log(prices[i+1]/prices[i]) for i in range(len(prices)-1)]
    total_log = math.log(prices[-1]/prices[0])
    log_data.append({
        'Stock': stock,
        'log(p0→p1)': log_returns[0], 
        'log(p1→p2)': log_returns[1], 
        'log(p2→p3)': log_returns[2], 
        'log(p3→p4)': log_returns[3], 
        'log(p0→p4)': total_log,     
        'sum(all)': sum(log_returns),
        'difference': sum(log_returns) - total_log
    })

df_log = pd.DataFrame(log_data)

# Portfolio (dari total)
pl = portfolio_sum.values
r_log = [math.log(pl[i+1]/pl[i]) for i in range(len(pl)-1)]
r_total = math.log(pl[-1]/pl[0])

df_log.loc[len(df_log)] = {
    'Stock': 'Return Portofolio (dari total)',
    'log(p0→p1)': r_log[0], 
    'log(p1→p2)': r_log[1], 
    'log(p2→p3)': r_log[2], 
    'log(p3→p4)': r_log[3], 
    'log(p0→p4)': r_total,     
    'sum(all)': sum(r_log),
    'difference': sum(r_log) - r_total
}

# Log returns dengan bobot
r_weighted = []
for i in range(4):
    weight_period = weights.iloc[i]
    weighted_r = sum(weight_period[s] * math.log(price_df.loc[s, f'p{i+1}']/price_df.loc[s, f'p{i}']) for s in tickers) # Modified index naming
    r_weighted.append(weighted_r)

df_log.loc[len(df_log)] = {
    'Stock': 'Portfolio (weighted sum)',
    'log(p0→p1)': r_weighted[0], 
    'log(p1→p2)': r_weighted[1], 
    'log(p2→p3)': r_weighted[2], 
    'log(p3→p4)': r_weighted[3], 
    'log(p0→p4)': sum(r_weighted),     
    'sum(all)': sum(r_weighted),
    'difference': sum(r_weighted) - sum(r_log)
}

# Difference
df_log.loc[len(df_log)] = {
    'Stock': 'Difference (totals − weighted)',
    'log(p0→p1)': r_log[0]-r_weighted[0], 
    'log(p1→p2)': r_log[1]-r_weighted[1], 
    'log(p2→p3)': r_log[2]-r_weighted[2], 
    'log(p3→p4)': r_log[3]-r_weighted[3], 
    'log(p0→p4)': r_total - sum(r_weighted),     
    'sum(all)': sum(r_log)-sum(r_weighted),
    'difference': (sum(r_log)-sum(r_weighted)) - (r_total - sum(r_weighted))
}

# exp(Portfolio dari total) - 1
df_log.loc[len(df_log)] = {
    'Stock': 'exp(Portfolio from totals) - 1',
    'log(p0→p1)': math.exp(r_log[0]) - 1, 
    'log(p1→p2)': math.exp(r_log[1]) - 1, 
    'log(p2→p3)': math.exp(r_log[2]) - 1, 
    'log(p3→p4)': math.exp(r_log[3]) - 1, 
    'log(p0→p4)': math.exp(r_total) - 1,     
    'sum(all)': sum([math.exp(x) - 1 for x in r_log]),
    'difference': (math.exp(r_total) - 1) - sum([math.exp(x) - 1 for x in r_log])
}


# Simple Return
spl_data = []
for stock in tickers:
    prices = price_df.loc[stock].values
    spl_returns = [(prices[i+1]-prices[i])/prices[i] for i in range(len(prices)-1)]
    total_spl = (prices[-1]-prices[0])/prices[0]
    spl_data.append({
        'Stock': stock,
        'spl(p0→p1)': spl_returns[0], 
        'spl(p1→p2)': spl_returns[1], 
        'spl(p2→p3)': spl_returns[2], 
        'spl(p3→p4)': spl_returns[3], 
        'spl(p0→p4)': total_spl,     
        'sum(all)': sum(spl_returns),
        'difference': sum(spl_returns) - total_spl
    })

df_spl = pd.DataFrame(spl_data)

# Portfolio (dari total)
r_spl = [(pl[i+1]-pl[i])/pl[i] for i in range(len(pl)-1)]
r_total_s = (pl[-1]-pl[0])/pl[0]

df_spl.loc[len(df_spl)] = {
    'Stock': 'Return Portofolio (dari totals)',
    'spl(p0→p1)': r_spl[0], 
    'spl(p1→p2)': r_spl[1], 
    'spl(p2→p3)': r_spl[2], 
    'spl(p3→p4)': r_spl[3], 
    'spl(p0→p4)': r_total_s,     
    'sum(all)': sum(r_spl),
    'difference': sum(r_spl) - r_total_s
}

# Simple Return dengan pembobotan
r_weighted_s = []
for i in range(4):
    weight_period = weights.iloc[i]
    weighted_s = sum(weight_period[s] * ((price_df.loc[s, f'p{i+1}'] - price_df.loc[s, f'p{i}']) / price_df.loc[s, f'p{i}']) for s in tickers) # Modified index naming
    r_weighted_s.append(weighted_s)

df_spl.loc[len(df_spl)] = {
    'Stock': 'Portfolio (weighted sum)',
    'spl(p0→p1)': r_weighted_s[0], 
    'spl(p1→p2)': r_weighted_s[1], 
    'spl(p2→p3)': r_weighted_s[2], 
    'spl(p3→p4)': r_weighted_s[3], 
    'spl(p0→p4)': sum(r_weighted_s),     
    'sum(all)': sum(r_weighted_s),
    'difference': sum(r_weighted_s) - sum(r_spl)
}

df_spl.loc[len(df_spl)] = {
    'Stock': 'Difference (totals − weighted)',
    'spl(p0→p1)': r_spl[0]-r_weighted_s[0], 
    'spl(p1→p2)': r_spl[1]-r_weighted_s[1], 
    'spl(p2→p3)': r_spl[2]-r_weighted_s[2], 
    'spl(p3→p4)': r_spl[3]-r_weighted_s[3], 
    'spl(p0→p4)': r_total_s - sum(r_weighted_s),     
    'sum(all)': sum(r_spl)-sum(r_weighted_s),
    'difference': (sum(r_spl)-sum(r_weighted_s)) - (r_total_s - sum(r_weighted_s))
}


# Tabel
pd.options.display.float_format = '{:,.0f}'.format
pd.options.display.width = None
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.expand_frame_repr = False
print("\n")
print("Harga Saham Akhir Tahun + Portofolio Total:")
print(price_df.round(2), "\n")
pd.options.display.float_format = '{:,.4f}'.format
print("Bobot Saham pada Portofolio:")
print(weights.round(4), "\n")

print("Log Return :")
print(df_log[['Stock', 'log(p0→p1)', 'log(p1→p2)', 'log(p2→p3)', 'log(p3→p4)', 'log(p0→p4)', 'sum(all)', 'difference']].round(4), "\n")

print("Simple Return :")
print(df_spl[['Stock', 'spl(p0→p1)', 'spl(p1→p2)', 'spl(p2→p3)', 'spl(p3→p4)', 'spl(p0→p4)', 'sum(all)', 'difference']].round(4))
