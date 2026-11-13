"""v18n-2 experiment 305."""
import numpy as np
import pandas as pd

FAMILY = "leanhog_cattleonfeed_report_repricing_continuation"
PARAMS = {"reference_end": 51300, "trade_start": 51360, "trade_end": 54000,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "HE" not in panel:
        return ans
    data = panel["HE"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    days, weekdays = calendar.dt.day.to_numpy(), calendar.dt.dayofweek.to_numpy()
    out = ans["HE"]
    for positions in data.groupby("session", sort=False).indices.values():
        first = positions[0]
        if not (weekdays[first] == 4 and 20 <= days[first] <= 28):
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 51300:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 51360 <= seconds[i] < 54000:
                if side * (close[i] - anchor) <= -0.625:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "HE" else 0.0)
            for symbol, data in panel.items()}
