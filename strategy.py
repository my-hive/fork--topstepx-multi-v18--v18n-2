"""v18n-2 experiment 288."""
import numpy as np

FAMILY = "microether_lateus_riskrepricing_reversal"
PARAMS = {"reference_start": 54000, "reference_end": 61200, "trade_start": 61260,
          "trade_end": 72000, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "MET" not in panel:
        return ans
    data = panel["MET"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["MET"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if 54000 <= seconds[i] <= 61200]
        trading = [i for i in positions if 61260 <= seconds[i] < 72000]
        if not reference or not trading:
            continue
        side = -1 if close[reference[-1]] >= close[reference[0]] else 1
        anchor = close[reference[-1]]
        for i in trading:
            if side * (close[i] - anchor) <= -2500:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "MET" else 0.0)
            for symbol, data in panel.items()}
