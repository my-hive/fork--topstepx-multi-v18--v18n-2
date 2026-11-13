"""v18n-2 experiment 274."""
import numpy as np

FAMILY = "nikkei_tokyoopen_orderflow_reversal"
PARAMS = {"reference_start": 61200, "reference_end": 64800, "trade_start": 64860,
          "trade_end": 75600, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "NKD" not in panel:
        return ans
    data = panel["NKD"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["NKD"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if 61200 <= seconds[i] <= 64800]
        trading = [i for i in positions if 64860 <= seconds[i] < 75600]
        if not reference or not trading:
            continue
        side = -1 if close[reference[-1]] >= close[reference[0]] else 1
        anchor = close[reference[-1]]
        for i in trading:
            if side * (close[i] - anchor) <= -50:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "NKD" else 0.0)
            for symbol, data in panel.items()}
