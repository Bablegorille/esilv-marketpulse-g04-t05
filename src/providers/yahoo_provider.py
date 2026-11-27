import yfinance as yf


def fetch_yahoo_prices(ticker, period="1mo", interval="1d"):
    """Récupère les prix Yahoo Finance au format canonique MarketPulse."""
    data = yf.Ticker(ticker).history(
        period=period,
        interval=interval,
        auto_adjust=False,
    )

    rows = []
    for index, row in data.iterrows():
        rows.append({
            "date": index.strftime("%Y-%m-%d"),
            "ticker": ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })

    return rows

