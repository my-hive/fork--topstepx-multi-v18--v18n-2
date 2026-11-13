"""v18n-2 experiment 270."""
import numpy as np
import pandas as pd

FAMILY = "australiandollar_asia_europe_handoff_continuation"
PARAMS = {"reference_start": 64800, "reference_end": 3600, "trade_start": 3660,
          "trade_end": 14400, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "6A" not in panel:
        return ans
    data = panel["6A"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["6A"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if seconds[i] >= 64800 or seconds[i] <= 3600]
        trading = [i for i in positions if 3660 <= seconds[i] < 14400]
        if not reference or not trading:
            continue
        side = 1 if close[reference[-1]] >= close[reference[0]] else -1
        anchor = close[reference[-1]]
        for i in trading:
            if side * (close[i] - anchor) <= -0.0025:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "6A" else 0.0)
            for symbol, data in panel.items()}
