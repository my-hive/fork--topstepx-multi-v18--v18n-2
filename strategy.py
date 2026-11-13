"""v18n-2 experiment 292."""
import numpy as np

FAMILY = "microaustraliandollar_tokyoopen_liquidity_reversal"
PARAMS = {"reference_end": 64800, "trade_start": 64860, "trade_end": 75600,
          "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "M6A" not in panel:
        return ans
    data = panel["M6A"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    out = ans["M6A"]
    for positions in data.groupby("session", sort=False).indices.values():
        anchor = None
        side = 0
        for i in positions:
            if seconds[i] == 64800:
                anchor = close[i]
                side = -1 if close[i] >= close[positions[0]] else 1
            elif anchor is not None and 64860 <= seconds[i] < 75600:
                if side * (close[i] - anchor) <= -0.002:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "M6A" else 0.0)
            for symbol, data in panel.items()}
