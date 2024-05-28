import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(start="2023-12-31", end="2024-03-31")
    beta = stock.info.get('beta', 'N/A')  # Use 'N/A' if 'beta' is not available
    return hist, beta

def fetch_all_stocks_data():
    stocks = {'AAPL': 100, 'MSFT': 100, 'VTI': 100}
    data = {}
    for ticker, shares in stocks.items():
        hist, beta = fetch_stock_data(ticker)
        data[ticker] = {'history': hist, 'shares': shares, 'beta': beta}
    return data
