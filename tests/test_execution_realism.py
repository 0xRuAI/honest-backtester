import numpy as np
import pandas as pd
import pytest

from backtester import BacktestConfig, Signal, Strategy, run_backtest
from backtester.exits import simulate_exit


class OneSignal(Strategy):
    def __init__(self, signal):
        self.signal = signal

    def generate_signals(self, df):
        return [self.signal]


def frame(rows):
    index = pd.date_range("2026-01-01", periods=len(rows), freq="h", tz="UTC")
    return pd.DataFrame(rows, columns=["open", "high", "low", "close", "volume"], index=index)


def test_limit_fill_does_not_claim_an_earlier_same_bar_target():
    df = frame(
        [
            (100, 101, 99, 100, 1),
            (100, 101, 99, 100, 1),
            (105, 112, 99, 101, 1),  # target and limit are both touched; order is unknown
            (101, 102, 94, 96, 1),
        ]
    )
    signal = Signal(1, "long", 100, 95, [110], entry_mode="limit", entry_window=2)

    result = run_backtest(df, OneSignal(signal), BacktestConfig())

    assert result["n_trades"] == 1
    assert result["_trades"][0].reason == "stop"
    assert result["_trades"][0].exit_index == 3


def test_market_entry_at_open_can_take_a_same_bar_target():
    df = frame(
        [
            (100, 101, 99, 100, 1),
            (100, 101, 99, 100, 1),
            (100, 112, 99, 111, 1),
            (111, 112, 94, 96, 1),
        ]
    )
    signal = Signal(1, "long", 100, 95, [110], entry_mode="market")

    result = run_backtest(df, OneSignal(signal), BacktestConfig())

    assert result["_trades"][0].reason == "target_first_full"
    assert result["_trades"][0].exit_index == 2


def test_market_entry_pays_taker_and_slippage():
    result = simulate_exit(
        high=np.array([111.0]),
        low=np.array([99.0]),
        close=np.array([110.0]),
        epoch_s=np.array([0]),
        entry_j=0,
        entry=100.0,
        stop=95.0,
        direction="long",
        t1=110.0,
        t_final=110.0,
        qty=1.0,
        partial=1.0,
        costs=(0.0005, 0.0002, 0.0003, 0.0, False),
        entry_taker=True,
    )

    assert result.cost == pytest.approx(0.102)
    assert result.net == pytest.approx(9.898)


def test_partial_then_breakeven_charges_the_remainder_exit_cost():
    result = simulate_exit(
        high=np.array([111.0]),
        low=np.array([99.0]),
        close=np.array([100.0]),
        epoch_s=np.array([0]),
        entry_j=0,
        entry=100.0,
        stop=90.0,
        direction="long",
        t1=110.0,
        t_final=120.0,
        qty=1.0,
        partial=0.5,
        costs=(0.0005, 0.0002, 0.0003, 0.0, False),
    )

    assert result.reason == "partial_then_stop"
    assert result.cost == pytest.approx(0.071)
    assert result.net == pytest.approx(4.929)


def test_legacy_entry_bar_target_behavior_can_be_enabled_explicitly():
    df = frame(
        [
            (100, 101, 99, 100, 1),
            (100, 101, 99, 100, 1),
            (105, 112, 99, 101, 1),
            (101, 102, 94, 96, 1),
        ]
    )
    signal = Signal(1, "long", 100, 95, [110], entry_mode="limit", entry_window=2)
    cfg = BacktestConfig(allow_limit_entry_bar_target=True)

    result = run_backtest(df, OneSignal(signal), cfg)

    assert result["_trades"][0].reason == "target_first_full"
