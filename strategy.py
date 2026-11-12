"""v18n-2 experiment 3.
FAMILY: gold_us_morning_range_breakout
Mechanism: GC range built 17:00-08:30 CT (Asia+London) holds resting stops; a COMEX-session
close beyond it triggers stop-run/CTA momentum that continues through the US morning.
Hypothesis: first completed 1m close beyond overnight range at/after 08:30 CT, one trade/session,
fixed $250 stop, flat 13:00 CT. GC only, 1 contract.
Falsification: <70% positive years, any negative era, or fold pass rates ~0.
"""
import numpy as np

FAMILY = "gold_us_morning_range_breakout"
PARAMS = {"entry_sec": 30600, "exit_sec": 46800, "stop_ticks": 25}
GC_TICK, GC_PV = 0.1, 100.0
RISK = PARAMS["stop_ticks"] * GC_TICK * GC_PV  # $250/contract


def signals(panel):
    res = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "GC":
            c, h, l, s = (df[k].to_numpy() for k in ("close", "high", "low", "ct_sec"))
            stop = PARAMS["stop_ticks"] * GC_TICK
            for idx in df.groupby("session", sort=False).indices.values():
                hi, lo, pos, ref, done = -np.inf, np.inf, 0, 0.0, False
                for i in idx:
                    t = s[i]
                    if t < PARAMS["entry_sec"]:
                        hi, lo = max(hi, h[i]), min(lo, l[i])
                    elif t < PARAMS["exit_sec"] and not done:
                        if pos == 0 and np.isfinite(hi):
                            pos = 1 if c[i] > hi else (-1 if c[i] < lo else 0)
                            ref = c[i]
                        elif pos and pos * (c[i] - ref) <= -stop:
                            pos, done = 0, True
                        out[i] = pos
        res[sym] = out
    return res


def entry_risk(panel):
    return {s: np.full(len(d), RISK if s == "GC" else 0.0) for s, d in panel.items()}
