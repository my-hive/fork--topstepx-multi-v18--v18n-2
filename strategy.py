"""v18n-2 experiment 298."""
import numpy as np

FAMILY = "microcrude_asia_uscommercial_liquidity_reversal"
PARAMS = {"reference_end": 27000, "trade_start": 27060, "trade_end": 36000,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "MCL" not in panel:
        return ans
    data = panel["MCL"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    out = ans["MCL"]
    for positions in data.groupby("session", sort=False).indices.values():
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 27000:
                anchor = close[i]
                side = -1 if close[i] >= close[positions[0]] else 1
            elif anchor is not None and 27060 <= seconds[i] < 36000:
                if side * (close[i] - anchor) <= -2.5:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "MCL" else 0.0)
            for symbol, data in panel.items()}
