"""v18n-2 experiment 9. Post-seed pivot.
FAMILY: gold_month_end_rebalance_long
Mechanism: month-end portfolio rebalancing and commodity-index roll demand creates
systematic gold buying near calendar month-end, distinct from intraday technical families.
Hypothesis: long GC from 17:00 CT on final two calendar trading sessions through 15:00 CT,
with a $250 completed-bar stop. No threshold fitted to returns.
Falsification: stressed PnL/any era negative or <70% positive years.
"""
import numpy as np
import pandas as pd

FAMILY = "gold_month_end_rebalance_long"
PARAMS = {"days_from_month_end": 2, "exit_sec": 54000, "stop_dollars": 250}
GC_PV = 100.0


def signals(panel):
    ans = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "GC":
            close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            # Calendar rule declared ex ante; weekends/holidays naturally do not trade.
            dates = pd.to_datetime(df.session)
            selected = (dates.dt.day > dates.dt.days_in_month - PARAMS["days_from_month_end"]).to_numpy()
            for idx in df.groupby("session", sort=False).indices.values():
                if not selected[idx[0]]:
                    continue
                ref = close[idx[0]]
                for i in idx[1:]:
                    if PARAMS["exit_sec"] <= sec[i] < 61200 or close[i] - ref <= -PARAMS["stop_dollars"] / GC_PV:
                        break
                    out[i] = 1
        ans[sym] = out
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), PARAMS["stop_dollars"] if s == "GC" else 0.0)
            for s, d in panel.items()}
