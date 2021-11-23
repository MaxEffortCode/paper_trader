import yfinance as yf
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

while(True):
    print("what ticker?:")
    ticker = input().upper()
    # define the ticker symbol
    tickerSymbol = ticker

    # get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    # get the historical prices for this ticker
    tickerDf = tickerData.history(
        period='1d', start='2000-1-1', end='2020-1-25')

    df = tickerDf[["High", "Low"]]
    df.plot.line()
    plt.xlabel("Year")
    plt.ylabel("Stripper & Coke Money")
    plt.title(f"Fat Fucking Gainz From: {ticker}")
    plt.show()