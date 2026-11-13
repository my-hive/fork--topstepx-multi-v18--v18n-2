"""v18n-2 experiment 288 causal repair."""
import numpy as np

FAMILY = "microether_lateus_riskrepricing_reversal"
PARAMS = {"reference_end": 61200, "trade_start": 61260, "trade_end": 72000,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "MET" not in panel:
        return ans
    data = panel["MET"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["MET"]
    for positions in data.groupby("session", sort=False).indices.values():
        last_ref = None
        for i in positions:
            if seconds[i] == 61200:
                last_ref = i
            if last_ref is not None and 61260 <= seconds[i] < 72000:
                side = -1 if close[last_ref] >= close[positions[0]] else 1
                if side * (close[i] - close[last_ref]) <= -2500:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "MET" else 0.0)
            for symbol, data in panel.items()}
