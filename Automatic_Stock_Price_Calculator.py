import requests
import pandas as pd
from datetime import datetime


def get_alpha_vantage_data(ticker, year, api_key):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "full",
        "apikey": api_key
    }


    response = requests.get(url, params=params)
    data = response.json()


    if "Time Series (Daily)" not in data:
        raise ValueError(f"Alpha Vantage error for {ticker}. Response: {data}")




    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close"
    })
    df = df[["Open", "High", "Low", "Close"]].astype(float)


    # Filter for the given year
    start_date = pd.to_datetime(f"{year}-01-01")
    end_date = pd.to_datetime(f"{year}-12-31")
    df = df[(df.index >= start_date) & (df.index <= end_date)]


    return df


def calculate_stock_statistics(stock_data):
    high_52_week = stock_data["High"].max()
    low_52_week = stock_data["Low"].min()
    yearly_avg = (stock_data["Open"].sum() + stock_data["Close"].sum()) / (2 * len(stock_data))
    return round(low_52_week, 2), round(high_52_week, 2), round(yearly_avg, 2)


# === USER SETTINGS ===
ticker = "FTS"
year_now = 2024
api_key = "U3BDU3SVGEI3GFJ5"  # Replace this with your real Alpha Vantage API key
# =====================


year_before = year_now - 1


# Get data
data_year_now = get_alpha_vantage_data(ticker, year_now, api_key)
data_year_before = get_alpha_vantage_data(ticker, year_before, api_key)


# Compute stats
low_now, high_now, avg_now = calculate_stock_statistics(data_year_now)
low_before, high_before, avg_before = calculate_stock_statistics(data_year_before)


# Create output
output_data = {
    "Metric": [f"52 Week Low in {year_now}", f"52 Week High in {year_now}", f"Yearly Average in {year_now}",
               f"52 Week Low in {year_before}", f"52 Week High in {year_before}", f"Yearly Average in {year_before}"],
    "Value": [low_now, high_now, avg_now, low_before, high_before, avg_before]
}


df = pd.DataFrame(output_data)
print(df.to_string(index=False))

