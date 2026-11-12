"""v18n-2 experiment 14. Claimed independent metals family:
FAMILY: metals_two_day_extreme_trend_continuation
Mechanism: completed two-day metal returns in the top 5% of their trailing 300-session
distribution signal macro/regime repricing. The next reopen continues the trend because
positioning/hedging executes after the close; only tails are traded, not routine moves.
Hypothesis: for each metal independently, enter at first 17:00 CT reopen bar after the
signal day in the direction of the two-day return; hold through next 15:00 CT, $250 stop,
one contract. Causal rolling quantile only. Pre-screen showed GC/SI/HG all positive and
multi-metal portfolio positive 13/13 active years.
Falsification: stressed PnL/era negative or fold pass ~0.
"""
import numpy as np

FAMILY = "metals_two_day_extreme_trend_continuation"
PARAMS = {"quantile": 0.95, "lookback_sessions": 300, "return_sessions": 2, "stop_dollars": 250}
PV = {"GC": 100.0, "SI": 5000.0, "HG": 25000.0, "PL": 50.0}
CLOSE_LO, CLOSE_HI = 53400, 54000
REOPEN_LO, REOPEN_HI = 61200, 61500
EXIT_SEC = 54000


def _plan(df, pv):
    out = np.zeros(len(df), dtype=np.int64)
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    closes, returns, history = [], [], []
    for idx in df.groupby("session", sort=False).indices.values():
        close_bars = [i for i in idx if CLOSE_LO <= sec[i] <= CLOSE_HI]
        reopen = [i for i in idx if REOPEN_LO <= sec[i] < REOPEN_HI]
        us_hours = [i for i in idx if 30600 <= sec[i] < EXIT_SEC]
        signal = None
        if len(closes) >= PARAMS["return_sessions"] and close_bars:
            signal = closes[-1] / closes[-PARAMS["return_sessions"]] - 1
        if close_bars:
            closes.append(close[close_bars[-1]])
        if signal is None:
            continue
        past = np.abs(history[-PARAMS["lookback_sessions"]:])
        history.append(signal)
        if len(past) < PARAMS["lookback_sessions"] or abs(signal) < np.quantile(past, PARAMS["quantile"]):
            continue
        bars = reopen + us_hours
        if len(bars) < 2:
            continue
        side, ref = int(np.sign(signal)), close[bars[0]]
        for i in bars[1:]:
            if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / pv:
                break
            out[i] = side
    return out


def signals(panel):
    return {s: (_plan(d, PV[s]) if s in PV else np.zeros(len(d), dtype=np.int64)) for s, d in panel.items()}


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s in PV else 0.0) for s, d in panel.items()}
