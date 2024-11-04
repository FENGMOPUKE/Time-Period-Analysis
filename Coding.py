import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import plotly.graph_objects as go
import yfinance as yf

# 1&2
data = yf.download("^GSPC ^IXIC GLD ^VIX", start="2007-01-01", end="2020-03-31")["Close"]
GLD = data[['GLD']].rename(columns={'GLD': 'Close'})
GSPC = data[['^GSPC']].rename(columns={'^GSPC': 'Close'})
IXIC = data[['^IXIC']].rename(columns={'^IXIC': 'Close'})
bear_market_start = "2007-01-01"
bear_market_end = "2009-03-31"
bull_market_start = "2009-03-31"
bull_market_end = "2020-01-31"
covid_crisis_start = "2020-01-31"
covid_crisis_end = "2020-03-31"
stocks = {'GSPC': GSPC, 
          'GLD': GLD, 
          'IXIC': IXIC}
stocks_bear_market = {}
stocks_bull_market = {}
stocks_covid_market = {}
def analyze_period(period_name, stock, start_date, end_date):
    df1 = stock[start_date: end_date]
    df1_returns = df1['Return']
    df1_cum_returns = df1['Cum Return']
    return df1
for stock in stocks.keys():
    stocks[stock]['Return'] = stocks[stock]['Close'].pct_change()
    stocks[stock]['Cum Return'] = (1 + stocks[stock]['Return']).cumprod()
    stocks_bear_market[stock] = analyze_period('bear', stocks[stock], bear_market_start, bear_market_end)
    stocks_bull_market[stock] = analyze_period('bull', stocks[stock], bull_market_start, bull_market_end)
    stocks_covid_market[stock] = analyze_period('covid', stocks[stock], covid_crisis_start, covid_crisis_end)

# 3
stock_cum_return = pd.DataFrame()
for stock in stocks.keys():
    stock_cum_return[stock] = stocks[stock]['Cum Return']
stock_cum_return
def plot_compare(dict1):
    for key in dict1.keys():
        dict1[key]['Cum Return'].plot(figsize = (15,6))
    plot.legend(dict1.keys())
    #data = pd.concat([df['Cum Return'] for df in dict1.values()], axis=1)
    #data.plot(figsize=(10,5), legend = dict1.keys())
def plot_compare2(fig, dict1, period_name):
    for key in dict1.keys():
        fig.add_trace(go.Scatter(x=dict1[key].index, y=dict1[key]['Cum Return'], mode='lines', name=key))
    fig.update_layout(
    title={'text':'Cumulative Performance of the ' + period_name},
    title_x=0.5, 
    xaxis=dict(
        title='Date',
    ),
    yaxis=dict(
        title='Return',
         ticksuffix="%"
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    )
