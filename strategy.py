"""v18n-2 experiment 281."""
import numpy as np

FAMILY = "soybean_cashopen_commercial_liquidity_reversal"
PARAMS = {"reference_start": 30600, "reference_end": 32400, "trade_start": 32460,
          "trade_end": 41400, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "ZS" not in panel:
        return ans
    data = panel["ZS"]
    close = data.close.to_numpy()
    seconds = data.ct_sec.to_numpy()
    out = ans["ZS"]
    for positions in data.groupby("session", sort=False).indices.values():
        reference = [i for i in positions if 30600 <= seconds[i] <= 32400]
        trading = [i for i in positions if 32460 <= seconds[i] < 41400]
        if not reference or not trading:
            continue
        side = -1 if close[reference[-1]] >= close[reference[0]] else 1
        anchor = close[reference[-1]]
        for i in trading:
            if side * (close[i] - anchor) <= -1.0:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "ZS" else 0.0)
            for symbol, data in panel.items()}
