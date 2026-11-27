
from analytics import (
    align_series,
    calculate_period_return,
    calculate_relative_performance,
    calculate_base_100,
)

from providers.yahoo_provider import fetch_yahoo_prices
from providers.symbols import get_yahoo_symbol


LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

PERIOD = "1mo"
INTERVAL = "1d"


def main():
    # Market configuration
    instrument = {
        "ticker": "AAPL",
        "name": "Apple Inc.",
    }

    benchmark = {
        "ticker": "SP500",
        "name": "S&P 500",
    }

    # Retrieve Yahoo Finance data
    instrument_prices = fetch_yahoo_prices(
        ticker=get_yahoo_symbol(instrument["ticker"]),
        period=PERIOD,
        interval=INTERVAL,
    )

    benchmark_prices = fetch_yahoo_prices(
        ticker=get_yahoo_symbol(benchmark["ticker"]),
        period=PERIOD,
        interval=INTERVAL,
    )

    if not instrument_prices or not benchmark_prices:
        raise ValueError("Yahoo Finance returned no market data.")

    # Restore canonical tickers
    for row in instrument_prices:
        row["ticker"] = instrument["ticker"]

    for row in benchmark_prices:
        row["ticker"] = benchmark["ticker"]

    # Align both series using TD07 analytics
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument or not aligned_benchmark:
        raise ValueError("No common dates found between AAPL and SP500.")

    # Calculate returns
    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    # Calculate Base 100
    instrument_base = calculate_base_100(aligned_instrument)
    benchmark_base = calculate_base_100(aligned_benchmark)

    # Display results
    print("=== MarketPulse ===")
    print()
    print("Provider: Yahoo Finance via yfinance")
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {LOOKBACK_LABEL}")
    print(f"Interval   : {INTERVAL_LABEL}")
    print()

    print("Market returns")
    print(f"Instrument return : {instrument_return:.2f}%")
    print(f"Benchmark return  : {benchmark_return:.2f}%")
    print()

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
    )
    print()

    print("Base 100")
    print(
        f"{instrument['ticker']} : "
        f"{instrument_base[0]['value']:.2f} -> "
        f"{instrument_base[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']} : "
        f"{benchmark_base[0]['value']:.2f} -> "
        f"{benchmark_base[-1]['value']:.2f}"
    )

    print()
    print("Observations")
    print(f"{instrument['ticker']}: {len(aligned_instrument)}")
    print(f"{benchmark['ticker']}: {len(aligned_benchmark)}")


if __name__ == "__main__":
    main()
