"""v18n-2 experiment 301."""
import numpy as np
import pandas as pd

FAMILY = "eminigold_monthly_optionsexpiry_hedge_reversal"
PARAMS = {"reference_end": 34200, "trade_start": 34260, "trade_end": 41400,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "QG" not in panel:
        return ans
    data = panel["QG"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    days = calendar.dt.day.to_numpy()
    weekdays = calendar.dt.dayofweek.to_numpy()
    out = ans["QG"]
    for positions in data.groupby("session", sort=False).indices.values():
        first = positions[0]
        if not (weekdays[first] == 4 and 15 <= days[first] <= 21):
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 34200:
                anchor = close[i]
                side = -1 if close[i] >= close[positions[0]] else 1
            elif anchor is not None and 34260 <= seconds[i] < 41400:
                if side * (close[i] - anchor) <= -5:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "QG" else 0.0)
            for symbol, data in panel.items()}
