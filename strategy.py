"""v18n-2 experiment 295."""
import numpy as np
import pandas as pd

FAMILY = "microrussell_june_reconstitution_close_continuation"
PARAMS = {"reference_end": 52200, "trade_start": 52260, "trade_end": 54000,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "M2K" not in panel:
        return ans
    data = panel["M2K"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    months, days, weekdays = calendar.dt.month.to_numpy(), calendar.dt.day.to_numpy(), calendar.dt.dayofweek.to_numpy()
    out = ans["M2K"]
    for positions in data.groupby("session", sort=False).indices.values():
        first = positions[0]
        if not (months[first] == 6 and weekdays[first] == 4 and 22 <= days[first] <= 28):
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 52200:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 52260 <= seconds[i] < 54000:
                if side * (close[i] - anchor) <= -5:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "M2K" else 0.0)
            for symbol, data in panel.items()}
