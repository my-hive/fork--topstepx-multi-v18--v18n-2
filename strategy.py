"""v18n-2 experiment 303."""
import numpy as np
import pandas as pd

FAMILY = "nikkei_fiscalyearend_repatriation_flow_continuation"
PARAMS = {"reference_end": 64800, "trade_start": 64860, "trade_end": 75600,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "NKD" not in panel:
        return ans
    data = panel["NKD"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    calendar = pd.to_datetime(data.session)
    months, days = calendar.dt.month.to_numpy(), calendar.dt.day.to_numpy()
    out = ans["NKD"]
    for positions in data.groupby("session", sort=False).indices.values():
        first = positions[0]
        if not (months[first] == 3 and days[first] >= 27):
            continue
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 64800:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 64860 <= seconds[i] < 75600:
                if side * (close[i] - anchor) <= -250:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "NKD" else 0.0)
            for symbol, data in panel.items()}
