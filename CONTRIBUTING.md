# Contributing

Thanks for helping make backtests harder to fool.

## Development setup

```bash
git clone https://github.com/0xRuAI/honest-backtester.git
cd honest-backtester
python -m venv .venv
# Activate .venv using your shell, then:
python -m pip install -e ".[dev]"
python -m pytest
```

## Pull requests

1. Open an issue first for behavior changes or larger features.
2. Keep each pull request focused on one execution or accounting rule.
3. Add a failing test that demonstrates the bias or bug before changing the engine.
4. Document the fill-order assumption when OHLC data cannot establish event order.
5. Do not commit credentials, proprietary strategies, exchange account data, or generated environments.

Bug reports are most useful when they include a minimal OHLCV frame, one signal,
the expected fill sequence, and the actual result.
