"""v18n-2 experiment 307."""
import numpy as np
import pandas as pd

FAMILY = "fiveyear_payrollrelease_duration_repricing_continuation"
PARAMS = {"reference_end": 32400, "trade_start": 32460, "trade_end": 39600,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "ZF" not in panel:
        return ans
    data = panel["ZF"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    days, weekdays = calendar.dt.day.to_numpy(), calendar.dt.dayofweek.to_numpy()
    out = ans["ZF"]
    for positions in data.groupby("session", sort=False).indices.values():
        first = positions[0]
        if not (weekdays[first] == 4 and days[first] <= 7):
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 32400:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 32460 <= seconds[i] < 39600:
                if side * (close[i] - anchor) <= -0.125:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "ZF" else 0.0)
            for symbol, data in panel.items()}
