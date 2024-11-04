import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import plotly.graph_objects as go
import yfinance as yf
data = yf.download("^GSPC ^IXIC GLD ^VIX", start="2007-01-01", end="2020-03-31")["Close"]
data.head()
