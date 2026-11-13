"""v18n-2 experiment 299."""
import numpy as np

FAMILY = "yen_tokyofixing_liquidity_reversal"
PARAMS = {"reference_end": 68100, "trade_start": 68160, "trade_end": 75600,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "6J" not in panel:
        return ans
    data = panel["6J"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    out = ans["6J"]
    for positions in data.groupby("session", sort=False).indices.values():
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 68100:
                anchor = close[i]
                side = -1 if close[i] >= close[positions[0]] else 1
            elif anchor is not None and 68160 <= seconds[i] < 75600:
                if side * (close[i] - anchor) <= -0.00002:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "6J" else 0.0)
            for symbol, data in panel.items()}
