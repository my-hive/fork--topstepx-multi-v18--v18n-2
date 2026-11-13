"""v18n-2 experiment 306."""
import numpy as np
import pandas as pd

FAMILY = "soybean_quarterlystocks_repricing_continuation"
PARAMS = {"reference_end": 40500, "trade_start": 40560, "trade_end": 46800,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "ZS" not in panel:
        return ans
    data = panel["ZS"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    months, days = calendar.dt.month.to_numpy(), calendar.dt.day.to_numpy()
    out = ans["ZS"]
    for positions in data.groupby("session", sort=False).indices.values():
        first = positions[0]
        if not (months[first] in (3, 6, 9, 12) and days[first] >= 28):
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 40500:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 40560 <= seconds[i] < 46800:
                if side * (close[i] - anchor) <= -1:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "ZS" else 0.0)
            for symbol, data in panel.items()}
