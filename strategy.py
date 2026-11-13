"""v18n-2 experiment 282."""
import numpy as np

FAMILY = "spx_premarket_cashopen_gap_reversal"
PARAMS = {"reference_start": 61200, "reference_end": 30600, "trade_start": 30660,
          "trade_end": 37800, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "ES" not in panel:
        return ans
    data = panel["ES"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["ES"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if seconds[i] >= 61200 or seconds[i] <= 30600]
        trading = [i for i in positions if 30660 <= seconds[i] < 37800]
        if not reference or not trading:
            continue
        side = -1 if close[reference[-1]] >= close[reference[0]] else 1
        anchor = close[reference[-1]]
        for i in trading:
            if side * (close[i] - anchor) <= -5:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "ES" else 0.0)
            for symbol, data in panel.items()}
