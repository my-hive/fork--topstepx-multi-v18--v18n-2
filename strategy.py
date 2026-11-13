"""v18n-2 experiment 297."""
import numpy as np

FAMILY = "platinum_comex_autodemand_liquidity_continuation"
PARAMS = {"reference_end": 25200, "trade_start": 25260, "trade_end": 32400,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "PL" not in panel:
        return ans
    data = panel["PL"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    out = ans["PL"]
    for positions in data.groupby("session", sort=False).indices.values():
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 25200:
                anchor = close[i]
                side = 1 if close[i] >= close[positions[0]] else -1
            elif anchor is not None and 25260 <= seconds[i] < 32400:
                if side * (close[i] - anchor) <= -25:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "PL" else 0.0)
            for symbol, data in panel.items()}
