"""v18n-2 experiment 291."""
import numpy as np

FAMILY = "microeuro_frankfurt_liquidity_reversal"
PARAMS = {"reference_end": 3600, "trade_start": 3660, "trade_end": 14400,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "M6E" not in panel:
        return ans
    data = panel["M6E"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    out = ans["M6E"]
    for positions in data.groupby("session", sort=False).indices.values():
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 3600:
                anchor = close[i]
                side = -1 if close[i] >= close[positions[0]] else 1
            elif anchor is not None and 3660 <= seconds[i] < 14400:
                if side * (close[i] - anchor) <= -0.002:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "M6E" else 0.0)
            for symbol, data in panel.items()}
