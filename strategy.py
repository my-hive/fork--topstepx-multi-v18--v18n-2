"""v18n-2 experiment 304."""
import numpy as np
import pandas as pd

FAMILY = "corn_usda_wasde_repricing_continuation"
PARAMS = {"reference_end": 40500, "trade_start": 40560, "trade_end": 46800,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "ZC" not in panel:
        return ans
    data = panel["ZC"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    day = pd.to_datetime(data.session).dt.day.to_numpy()
    out = ans["ZC"]
    for positions in data.groupby("session", sort=False).indices.values():
        if not 9 <= day[positions[0]] <= 13:
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 40500:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 40560 <= seconds[i] < 46800:
                if side * (close[i] - anchor) <= -0.125:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "ZC" else 0.0)
            for symbol, data in panel.items()}
