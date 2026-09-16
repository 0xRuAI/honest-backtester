# Bundled data provenance

The CSV files under `data/` are a reproducibility convenience, not an
authoritative market-data product. They contain public OHLCV candles fetched
through `ccxt`; the swap-style filenames identify linear USDT instruments.
The files do not embed a complete immutable venue/request manifest, so users
who need auditable data should fetch fresh bars from their chosen venue.

To create a separate cache of Binance linear-swap bars:

```bash
python download_data.py --exchange binance --market-type swap \
  --symbols BTC/USDT:USDT,ETH/USDT:USDT --timeframes 1h,15m --years 3 \
  --data-dir ./my-data
```

Exchange candles can differ because of venue, contract, outage, correction,
and currently-forming-bar behavior. Record the exchange, market type, symbols,
timeframes, download time, and `ccxt` version with any published result.
