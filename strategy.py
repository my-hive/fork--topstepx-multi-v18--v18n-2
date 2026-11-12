"""v18n-2 experiment 31. Independent metals family.
FAMILY: metals_thursday_loss_friday_rebound
Mechanism: after a down Thursday, pre-weekend risk reduction and short covering should be
strongest in Friday's metals session; the effect is only used after a completed weak day.
Hypothesis: if prior completed session return is negative and next session is Friday, go
long GC/SI/HG from first 17:00 CT bar through 15:00 CT, $250 stop. No fitted thresholds.
Falsification: stressed PnL/any era negative or year fraction <70%.
"""
import numpy as np
import pandas as pd

FAMILY = "metals_thursday_loss_friday_rebound"
PARAMS = {"stop_dollars": 250}
PV = {"GC": 100.0, "SI": 5000.0, "HG": 25000.0}


def _plan(df, pv):
    out = np.zeros(len(df), dtype=np.int64)
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    prior, weak = None, False
    for idx in df.groupby("session", sort=False).indices.values():
        day = pd.Timestamp(df.session.iloc[idx[0]]).dayofweek
        bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
        if weak and day == 4 and len(bars) > 1:
            ref = close[bars[0]]
            for i in bars[1:]:
                if close[i] - ref <= -PARAMS["stop_dollars"] / pv:
                    break
                out[i] = 1
        end = [i for i in idx if 53400 <= sec[i] <= 54000]
        if end:
            px = close[end[-1]]
            weak = prior is not None and px < prior
            prior = px
    return out


def signals(panel):
    return {s: (_plan(d, PV[s]) if s in PV else np.zeros(len(d), dtype=np.int64)) for s, d in panel.items()}


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s in PV else 0.0) for s, d in panel.items()}
