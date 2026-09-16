# Changelog

All notable changes are documented here. This project follows semantic versioning.

## 0.2.0 - 2026-09-16

### Fixed

- Prevented conservative limit fills from claiming a take-profit on the entry
  bar when OHLC data cannot prove that the target happened after the fill.
- Charged the missing taker fee and slippage when a post-partial remainder exits
  at breakeven.
- Charged market entries as taker executions with slippage instead of maker fills.
- Allowed a valid signal decided on the first input bar to fill on the next bar.
- Rejected invalid partial fractions outside the `(0, 1]` interval.

### Added

- Regression tests for fill ordering, cost accounting, sizing, and risk guards.
- Installable package metadata and optional dependency groups.
- GitHub Actions tests for Python 3.9, 3.11, and 3.13.
- Contribution, security, conduct, and data-provenance documentation.

## 0.1.0 - 2026-07-07

- Initial public engine, example strategies, downloader, charts, sweeps, and
  bundled OHLCV sample data.
