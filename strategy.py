"""v18n-2 experiment 272."""
import numpy as np

FAMILY = "sterling_londonopen_liquidity_reversal"
PARAMS = {"reference_start": 79200, "reference_end": 7200, "trade_start": 7260,
          "trade_end": 18000, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "6B" not in panel:
        return ans
    data = panel["6B"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["6B"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if seconds[i] >= 79200 or seconds[i] <= 7200]
        trading = [i for i in positions if 7260 <= seconds[i] < 18000]
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
    return {symbol: np.full(len(data), 250.0 if symbol == "6B" else 0.0)
            for symbol, data in panel.items()}
