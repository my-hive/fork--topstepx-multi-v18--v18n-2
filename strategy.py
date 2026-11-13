"""v18n-2 experiment 290."""
import numpy as np
import pandas as pd

FAMILY = "spx_monthly_optionsexpiry_dealergamma_reversal"
PARAMS = {"reference_end": 36000, "trade_start": 46800, "trade_end": 52200,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "ES" not in panel:
        return ans
    data = panel["ES"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    days = calendar.dt.day.to_numpy()
    weekdays = calendar.dt.dayofweek.to_numpy()
    out = ans["ES"]
    for positions in data.groupby("session", sort=False).indices.values():
        if weekdays[positions[0]] != 4 or not 15 <= days[positions[0]] <= 21:
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 36000:
                anchor = close[i]
                side = -1 if close[i] >= close[positions[0]] else 1
            elif anchor is not None and 46800 <= seconds[i] < 52200:
                if side * (close[i] - anchor) <= -5:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "ES" else 0.0)
            for symbol, data in panel.items()}
