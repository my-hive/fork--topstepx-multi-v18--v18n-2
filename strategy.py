"""v18n-2 experiment 15. Independent metals family:
FAMILY: silver_daily_extreme_close_continuation
Mechanism: an extreme completed one-day SI close-to-close move (top 5% versus trailing
300 sessions) marks major macro repricing; next-session overnight/early flow continues it
because hedging and positioning complete after the signal close.
Hypothesis: enter 1 SI contract at first 17:00 CT reopen bar following the signal close,
hold through the next 15:00 CT close, with $250 stop. Causal quantile uses past only.
Falsification: stressed PnL or any era negative, or year coverage below robust threshold.
"""
import numpy as np

FAMILY = "silver_daily_extreme_close_continuation"
PARAMS = {"quantile": 0.95, "lookback_sessions": 300, "stop_dollars": 250}
SI_PV = 5000.0


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "SI" not in panel:
        return ans
    df = panel["SI"]
    out = ans["SI"]
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    prior_close, history = None, []
    for idx in df.groupby("session", sort=False).indices.values():
        close_bars = [i for i in idx if 53400 <= sec[i] <= 54000]
        reopen = [i for i in idx if 61200 <= sec[i] < 61500]
        us_hours = [i for i in idx if 30600 <= sec[i] < 54000]
        move = None
        if prior_close is not None and close_bars:
            move = close[close_bars[-1]] / prior_close - 1
        if close_bars:
            prior_close = close[close_bars[-1]]
        if move is None:
            continue
        past = np.abs(history[-PARAMS["lookback_sessions"]:])
        history.append(move)
        if len(past) < PARAMS["lookback_sessions"] or abs(move) < np.quantile(past, PARAMS["quantile"]):
            continue
        bars = reopen + us_hours
        if len(bars) < 2:
            continue
        side, ref = int(np.sign(move)), close[bars[0]]
        for i in bars[1:]:
            if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / SI_PV:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "SI" else 0.0) for s, d in panel.items()}
