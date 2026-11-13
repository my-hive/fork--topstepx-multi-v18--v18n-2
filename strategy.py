"""v18n-2 experiment 302."""
import numpy as np
import pandas as pd

FAMILY = "microdow_quarterly_optionsexpiry_close_continuation"
PARAMS = {"reference_end": 46800, "trade_start": 46860, "trade_end": 54000,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "MYM" not in panel:
        return ans
    data = panel["MYM"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    months, days, weekdays = calendar.dt.month.to_numpy(), calendar.dt.day.to_numpy(), calendar.dt.dayofweek.to_numpy()
    out = ans["MYM"]
    for positions in data.groupby("session", sort=False).indices.values():
        first = positions[0]
        if not (months[first] in (3, 6, 9, 12) and weekdays[first] == 4 and 15 <= days[first] <= 21):
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 46800:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 46860 <= seconds[i] < 54000:
                if side * (close[i] - anchor) <= -250:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "MYM" else 0.0)
            for symbol, data in panel.items()}
