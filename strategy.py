"""v18n-2 experiment 283."""
import numpy as np

FAMILY = "swissfranc_europeanclose_safehaven_reversal"
PARAMS = {"reference_start": 25200, "reference_end": 37800, "trade_start": 37860,
          "trade_end": 50400, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "6S" not in panel:
        return ans
    data = panel["6S"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["6S"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if 25200 <= seconds[i] <= 37800]
        trading = [i for i in positions if 37860 <= seconds[i] < 50400]
        if not reference or not trading:
            continue
        side = -1 if close[reference[-1]] >= close[reference[0]] else 1
        anchor = close[reference[-1]]
        for i in trading:
            if side * (close[i] - anchor) <= -0.002:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "6S" else 0.0)
            for symbol, data in panel.items()}
