"""v18n-2 experiment 32.
FAMILY: silver_monday_weekend_premium_fade
Mechanism: weekend headline/safe-haven demand is bid into silver at the Sunday reopen; thin
Sunday liquidity overshoots and the premium bleeds through the Monday-labelled session.
Hypothesis: short 1 SI from first bar of Monday-labelled session (Sun 17:00 CT) to Mon 15:00 CT,
$250 stop. Caveat: selected from a 5-weekday screen (post-hoc, ~5 looks); exact test only.
Falsification: stressed PnL/any era negative or year fraction <70%.
"""
import numpy as np
import pandas as pd

FAMILY = "silver_monday_weekend_premium_fade"
PARAMS = {"stop_dollars": 250}
SI_PV = 5000.0


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "SI" not in panel:
        return ans
    df, out = panel["SI"], ans["SI"]
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    for idx in df.groupby("session", sort=False).indices.values():
        if pd.Timestamp(df.session.iloc[idx[0]]).dayofweek != 0:
            continue
        bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
        if len(bars) < 2:
            continue
        ref = close[bars[0]]
        for i in bars[1:]:
            if -(close[i] - ref) <= -PARAMS["stop_dollars"] / SI_PV:
                break
            out[i] = -1
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "SI" else 0.0) for s, d in panel.items()}
