"""v18n-2 experiment 6.
FAMILY: gold_us_morning_range_breakout
Mechanism: GC overnight range 17:00-08:30 CT accumulates resting stops at its edges;
on high-range days a COMEX close beyond the edge triggers stop-run/CTA momentum that
persists into the US afternoon. Narrow overnight ranges carry no fuel - filtered out.
Hypothesis: on days with overnight range >= $10, enter first completed close beyond the
range at/after 08:30 CT, $250 stop, one trade/session, flat 15:00 CT. GC 1 contract.
Vectorized pre-screen: +$50k total, 10/14 positive years, all 3 eras positive.
Falsification: <70% positive years, any negative era, or worst-three fold pass ~0.
"""
import numpy as np

FAMILY = "gold_us_morning_range_breakout"
PARAMS = {"entry_sec": 30600, "exit_sec": 54000, "stop_dollars": 250, "min_range_pts": 10.0}
GC_PV = 100.0


def signals(panel):
    res = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "GC":
            c, h, l, s = (df[k].to_numpy() for k in ("close", "high", "low", "ct_sec"))
            stop = PARAMS["stop_dollars"] / GC_PV
            for idx in df.groupby("session", sort=False).indices.values():
                hi, lo, j = -np.inf, np.inf, 0
                while j < len(idx) and (s[idx[j]] >= 61200 or s[idx[j]] < PARAMS["entry_sec"]):
                    hi, lo = max(hi, h[idx[j]]), min(lo, l[idx[j]])
                    j += 1
                if not np.isfinite(hi) or hi - lo < PARAMS["min_range_pts"]:
                    continue
                pos, ref, done = 0, 0.0, False
                for k in idx[j:]:
                    if s[k] >= PARAMS["exit_sec"]:
                        break
                    if done:
                        continue
                    if pos == 0:
                        if c[k] > hi:
                            pos, ref = 1, c[k]
                        elif c[k] < lo:
                            pos, ref = -1, c[k]
                    elif pos * (c[k] - ref) <= -stop:
                        pos, done = 0, True
                    out[k] = pos
        res[sym] = out
    return res


def entry_risk(panel):
    # $250 stop + 2 ticks stressed slippage on the stop exit.
    risk = PARAMS["stop_dollars"] + 40.0
    return {s: np.full(len(d), risk if s == "GC" else 0.0) for s, d in panel.items()}
