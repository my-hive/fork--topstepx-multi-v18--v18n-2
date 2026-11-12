"""v18n-2 experiment 4. Claimed family:
FAMILY: metals_friday_long
Mechanism: gold/silver exhibit a Friday-session long premium (GC +12bp/day, t=3.1;
SI +14.6bp) - plausible short-hedging weekend cover and long-side weekend demand
flow; scan shows 12/14 (GC) and 11/14 (SI) positive years, all near-zero other weekdays.
Hypothesis: long GC+SI 1 contract each from Friday-session open (Thu 17:00 CT) to
15:00 CT Friday, $250/contract hard stop. Falsification: <70% positive years, any
negative era block, or PnL concentrated in one era.
"""
import numpy as np
import pandas as pd

FAMILY = "metals_friday_long"
PARAMS = {"stop_dollars": 250, "exit_sec": 54000}
SPECS = {"MGC": (0.1, 10.0), "SIL": (0.005, 1000.0)}


def _plan(df, tick, pv):
    out = np.zeros(len(df), dtype=np.int64)
    stop = PARAMS["stop_dollars"] / pv
    c, s = df.close.to_numpy(), df.ct_sec.to_numpy()
    for idx in df.groupby("session", sort=False).indices.values():
        day = pd.Timestamp(df.session.iloc[idx[0]]).day_of_week
        if day != 4 or len(idx) < 2:  # Friday sessions only
            continue
        ref = c[idx[0]]
        for i in idx[1:]:
            if s[i] >= PARAMS["exit_sec"] or c[i] - ref <= -stop:
                break
            out[i] = 1
    return out


def signals(panel):
    return {s: (_plan(d, *SPECS[s]) if s in SPECS else np.zeros(len(d), dtype=np.int64))
            for s, d in panel.items()}


def entry_risk(panel):
    return {s: np.full(len(d), float(PARAMS["stop_dollars"]) if s in SPECS else 0.0)
            for s, d in panel.items()}
