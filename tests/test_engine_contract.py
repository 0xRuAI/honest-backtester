import pandas as pd

from backtester import BacktestConfig, Signal, Strategy, run_backtest
from backtester.sizing import order_risk_ok, size_position


class Signals(Strategy):
    def __init__(self, *signals):
        self.signals = list(signals)

    def generate_signals(self, df):
        return self.signals


def prices(*rows):
    return pd.DataFrame(
        rows,
        columns=["open", "high", "low", "close", "volume"],
        index=pd.date_range("2026-01-01", periods=len(rows), freq="h", tz="UTC"),
    )


def test_signal_on_first_bar_fills_on_second_bar_without_lookahead():
    df = prices((100, 101, 99, 100, 1), (100, 111, 99, 110, 1))
    signal = Signal(0, "long", 100, 95, [110], entry_mode="market")

    result = run_backtest(df, Signals(signal))

    assert result["n_trades"] == 1
    assert result["_trades"][0].entry_index == 1


def test_penetration_threshold_rejects_a_touch_only_limit_fill():
    df = prices(
        (100, 101, 100, 100, 1),
        (100, 101, 100, 100, 1),
        (101, 102, 100, 101, 1),
    )
    signal = Signal(0, "long", 100, 95, [110], entry_mode="limit", entry_window=1)

    result = run_backtest(df, Signals(signal), BacktestConfig(fill_eps=0.001))

    assert result["n_trades"] == 0


def test_invalid_partial_fraction_is_rejected():
    df = prices((100, 101, 99, 100, 1), (100, 111, 99, 110, 1))
    signal = Signal(0, "long", 100, 95, [110], entry_mode="market", partial=1.5)

    result = run_backtest(df, Signals(signal))

    assert result["n_trades"] == 0


def test_tight_stop_filter_prevents_exploding_quantity():
    qty = size_position(
        equity=10_000,
        entry=100,
        stop=99.99,
        risk_mode="fixed",
        risk_per_trade=100,
        min_stop_dist_pct=0.001,
    )

    assert qty == 0


def test_risk_guard_rejects_notional_over_leverage_limit():
    ok, reason = order_risk_ok(
        entry=100,
        stop=99,
        qty=1_000,
        equity=1_000,
        risk_mode="fixed",
        risk_per_trade=1_000,
        leverage=2,
    )

    assert not ok
    assert "notional" in reason
