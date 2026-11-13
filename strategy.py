"""v18n-2 experiment 287."""
import numpy as np

FAMILY = "mexicanpeso_asia_liquidity_reversal"
PARAMS = {"reference_start": 64800, "reference_end": 75600, "trade_start": 75660,
          "trade_end": 3600, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "6M" not in panel:
        return ans
    data = panel["6M"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["6M"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if 64800 <= seconds[i] <= 75600]
        trading = [i for i in positions if seconds[i] >= 75660 or seconds[i] < 3600]
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
    return {symbol: np.full(len(data), 250.0 if symbol == "6M" else 0.0)
            for symbol, data in panel.items()}
