YAHOO_SYMBOLS={
    "AAPL":"AAPL",
    "SP500":"^GSPC",}


def get_yahoo_symbol(canonical_ticker):
    if canonical_ticker not in YAHOO_SYMBOLS:
        raise ValueError(
            f"Unsupported ticker for Yahoo Finance:{canonical_ticker}"
        )
    return YAHOO_SYMBOLS[canonical_ticker]