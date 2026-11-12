"""v18n-2 experiment 18. Independent metals family:
FAMILY: gold_month_of_year_long
Mechanism: ex-ante calendar demand for gold is hypothesized strongest in August/September
(Asian festival/stockbuilding) and January/February (new-year/asset-allocation and Lunar
New Year flow). This is a calendar premise, not an intraday technical signal.
Hypothesis: long 1 GC contract from first 17:00 CT reopen in those calendar months through
each 15:00 CT close, $250 completed-bar stop. Falsification: negative stressed total/era.
"""
import numpy as np
import pandas as pd

FAMILY = "gold_month_of_year_long"
PARAMS = {"months": [1, 2, 8, 9], "stop_dollars": 250, "exit_sec": 54000}
GC_PV = 100.0


def signals(panel):
    ans = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "GC":
            close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            month = pd.to_datetime(df.session).month.to_numpy()
            for idx in df.groupby("session", sort=False).indices.values():
                if month[idx[0]] not in PARAMS["months"]:
                    continue
                ref = close[idx[0]]
                for i in idx[1:]:
                    if 54000 <= sec[i] < 61200 or close[i] - ref <= -PARAMS["stop_dollars"] / GC_PV:
                        break
                    out[i] = 1
        ans[sym] = out
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "GC" else 0.0) for s, d in panel.items()}
