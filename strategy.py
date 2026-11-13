"""v18n-2 experiment 269."""
import numpy as np
import pandas as pd

FAMILY = "naturalgas_weekly_storage_release_reversal"
PARAMS = {"release_start": 34200, "release_end": 35100, "trade_start": 35160,
          "trade_end": 43200, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "NG" not in panel:
        return ans
    data = panel["NG"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    weekday = pd.to_datetime(data.session).dt.weekday.to_numpy()
    out = ans["NG"]
    for positions in data.groupby("session", sort=False).indices.values():
        release = [i for i in positions if 34200 <= seconds[i] <= 35100]
        trading = [i for i in positions if 35160 <= seconds[i] < 43200]
        if weekday[positions[0]] != 3 or not release or not trading:
            continue
        side = -1 if close[release[-1]] >= close[release[0]] else 1
        anchor = close[release[-1]]
        for i in trading:
            if side * (close[i] - anchor) <= -0.05:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "NG" else 0.0)
            for symbol, data in panel.items()}
