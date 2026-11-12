"""v18n-2 experiment 10 (metals pivot).
FAMILY: metals_extreme_overnight_continuation
Mechanism: an overnight (17:00-08:30 CT) move >=3x its trailing typical size usually
reflects macro/news repricing; US cash-hour participants take time to absorb it, so the
move continues intraday. Small moves are noise and are skipped.
Hypothesis: GC/SI/PL, |overnight return / median |overnight| of prior 60 sessions| >= 3 ->
trade in move direction from first bar >= 09:35 CT (past the 08:30-09:30 entry-diversity
window), $250 stop, flat 15:00 CT. Pre-screen (08:30 entry, gross): GC +$102, SI +$92, PL +$63/trade.
Falsification: stressed PnL negative, any era negative, or <70% positive years.
"""
import numpy as np

FAMILY = "metals_extreme_overnight_continuation"
PARAMS = {"z_min": 3.0, "vol_sessions": 60, "entry_sec": 34500, "exit_sec": 54000, "stop_dollars": 250}
PV = {"GC": 100.0, "SI": 5000.0, "PL": 50.0}


def _plan(df, pv):
    out = np.zeros(len(df), dtype=np.int64)
    c, s = df.close.to_numpy(), df.ct_sec.to_numpy()
    stop = PARAMS["stop_dollars"] / pv
    hist = []
    for idx in df.groupby("session", sort=False).indices.values():
        pre = [i for i in idx if s[i] >= 61200 or s[i] < 30540]
        post = [i for i in idx if PARAMS["entry_sec"] <= s[i] < PARAMS["exit_sec"]]
        if len(pre) < 2:
            continue
        on = c[pre[-1]] / c[pre[0]] - 1
        past = hist[-PARAMS["vol_sessions"]:]
        hist.append(abs(on))  # appended after use of past only
        if len(past) < PARAMS["vol_sessions"] or not post:
            continue
        typ = np.median(past)
        if typ <= 0 or abs(on) < PARAMS["z_min"] * typ:
            continue
        side, ref = int(np.sign(on)), c[post[0]]
        for i in post:
            if side * (c[i] - ref) <= -stop:
                break
            out[i] = side
    return out


def signals(panel):
    return {s: (_plan(d, PV[s]) if s in PV else np.zeros(len(d), dtype=np.int64)) for s, d in panel.items()}


def entry_risk(panel):
    return {s: np.full(len(d), PARAMS["stop_dollars"] + 40.0 if s in PV else 0.0) for s, d in panel.items()}
