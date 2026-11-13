"""v18n-2 experiment 300."""
import numpy as np
import pandas as pd

FAMILY = "micronaturalgas_weekly_storage_repricing_continuation"
PARAMS = {"reference_end": 35100, "trade_start": 35160, "trade_end": 41400,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "MNG" not in panel:
        return ans
    data = panel["MNG"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    weekdays = pd.to_datetime(data.session).dt.dayofweek.to_numpy()
    out = ans["MNG"]
    for positions in data.groupby("session", sort=False).indices.values():
        if weekdays[positions[0]] != 3:
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 35100:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 35160 <= seconds[i] < 41400:
                if side * (close[i] - anchor) <= -0.25:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "MNG" else 0.0)
            for symbol, data in panel.items()}
