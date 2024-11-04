import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import plotly.graph_objects as go
import statsmodels.api as sm

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

def plot_compare(dict1):
    for key in dict1.keys():
        dict1[key]['Cum Return'].plot(figsize = (15,6))
    plot.legend(dict1.keys())

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
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


# 4
fig1 = plot_compare2(go.Figure(), stocks, 'Entire Period')
fig1.show()

fig2 = plot_compare2(go.Figure(), stocks_bear_market, 'Bear Market')
fig2.show()

fig3 = plot_compare2(go.Figure(), stocks_bull_market, 'Bull Market')
fig3.show()

fig4 = plot_compare2(go.Figure(), stocks_covid_market, 'Covid Period')
fig4.show()

stock_return = pd.DataFrame()
stock_return['GSPC'] = data['^GSPC'].pct_change()
stock_return['IXIC'] = data['^IXIC'].pct_change()
stock_return['GLD'] = data['GLD'].pct_change()
stock_return['VIX'] = data['^VIX'].pct_change()


#5
def df_subset(df, start, point1, point2, end):
    df1 = df[start : point1]
    df2 = df[point1 : point2]
    df3 = df[point2 : end]
    return pd.DataFrame(df1), pd.DataFrame(df2), pd.DataFrame(df3)

GSPC_bear, GSPC_bull, GSPC_covid = df_subset(stock_return['GSPC'], "2007-01-01", "2009-03-31", "2020-01-31", "2020-03-31")
GLD_bear, GLD_bull, GLD_covid = df_subset(stock_return['GLD'], "2007-01-01", "2009-03-31", "2020-01-31", "2020-03-31")
IXIC_bear, IXIC_bull, IXIC_covid = df_subset(stock_return['IXIC'], "2007-01-01", "2009-03-31", "2020-01-31", "2020-03-31")
VIX_bear, VIX_bull, VIX_covid = df_subset(stock_return['VIX'], "2007-01-01", "2009-03-31", "2020-01-31", "2020-03-31")

bear_correlation = pd.concat([GSPC_bear, GLD_bear, IXIC_bear, VIX_bear], axis = 1).corr()
print(bear_correlation)

bull_correlation = pd.concat([GSPC_bull, GLD_bull, IXIC_bull, VIX_bull], axis = 1).corr()
print(bull_correlation)

covid_correlation = pd.concat([GSPC_covid, GLD_covid, IXIC_covid, VIX_covid], axis = 1).corr()
print(covid_correlation)

def beta_cal(Y_list, X):
    beta_list = []
    for Y in Y_list:
        model = sm.OLS(Y,X,missing="drop").fit()
        beta_list.append(model.params['GSPC'])
    return beta_list

beta_bear = beta_cal([GLD_bear, VIX_bear], GSPC_bear)
beta_bull = beta_cal([GLD_bull, VIX_bull], GSPC_bull)
beta_covid = beta_cal([GLD_covid, VIX_covid], GSPC_covid)
beta_list = [beta_bear, beta_bear, beta_bear]
print(beta_list)
