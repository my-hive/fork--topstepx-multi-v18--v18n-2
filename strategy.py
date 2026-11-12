"""v18n-2 experiment 20. Independent metals trend/regime family:
FAMILY: gold_daily_trend_regime_long
Mechanism: gold's medium-horizon risk premium is state-dependent; trend-following uses
prior 20-session sign, intended to hold during persistent macro regimes and avoid
mean-reverting drawdown states.
Hypothesis: if prior completed 20-session return is positive, long 1 GC contract from
17:00 CT reopen through 15:00 CT next session, $250 stop. One contract.
Falsification: stressed PnL/any era negative or <70% years.
"""
import numpy as np

FAMILY = "gold_daily_trend_regime_long"
PARAMS = {"lookback_sessions": 20, "stop_dollars": 250}
GC_PV = 100.0


def signals(panel):
    ans = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "GC":
            close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            closes = []
            for idx in df.groupby("session", sort=False).indices.values():
                bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
                active = len(closes) >= PARAMS["lookback_sessions"] and closes[-1] / closes[-PARAMS["lookback_sessions"]] > 1
                close_bars = [i for i in idx if 53400 <= sec[i] <= 54000]
                if close_bars:
                    closes.append(close[close_bars[-1]])
                if active and len(bars) > 1:
                    ref = close[bars[0]]
                    for i in bars[1:]:
                        if close[i] - ref <= -PARAMS["stop_dollars"] / GC_PV:
                            break
                        out[i] = 1
        ans[sym] = out
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "GC" else 0.0) for s, d in panel.items()}
