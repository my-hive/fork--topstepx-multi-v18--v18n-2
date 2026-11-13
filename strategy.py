"""v18n-2 experiment 294."""
import numpy as np

FAMILY = "microsterling_londonfixing_liquidity_reversal"
PARAMS = {"reference_end": 18000, "trade_start": 18060, "trade_end": 25200,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "M6B" not in panel:
        return ans
    data = panel["M6B"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    out = ans["M6B"]
    for positions in data.groupby("session", sort=False).indices.values():
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 18000:
                anchor = close[i]
                side = -1 if close[i] >= close[positions[0]] else 1
            elif anchor is not None and 18060 <= seconds[i] < 25200:
                if side * (close[i] - anchor) <= -0.002:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "M6B" else 0.0)
            for symbol, data in panel.items()}
