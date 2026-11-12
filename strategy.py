"""v18n-2 experiment 19. Independent metals statistical family:
FAMILY: gold_week_of_month_long
Mechanism: ex-ante monthly settlement/index-flow patterns may cluster by week number;
weeks 2 and 3 are selected as mid-month positioning/risk-on windows, not fitted thresholds.
Hypothesis: long 1 GC contract from 17:00 CT session open through 15:00 CT on session days
falling in calendar weeks 2-3, $250 stop. Falsification: negative stressed PnL/era.
"""
import numpy as np
import pandas as pd

FAMILY = "gold_week_of_month_long"
PARAMS = {"weeks": [2, 3], "stop_dollars": 250, "exit_sec": 54000}
GC_PV = 100.0


def signals(panel):
    ans = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "GC":
            close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            week = (((pd.to_datetime(df.session).dt.day - 1) // 7) + 1).to_numpy()
            for idx in df.groupby("session", sort=False).indices.values():
                if week[idx[0]] not in PARAMS["weeks"]:
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
