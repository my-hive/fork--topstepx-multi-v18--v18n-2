"""v18n-2 experiment 289."""
import numpy as np
import pandas as pd

FAMILY = "bitcoin_weekend_handoff_asia_liquidity_reversal"
PARAMS = {"friday_reference_end": 61200, "trade_start": 61260,
          "trade_end": 72000, "stop_dollars": 250}


def signals(panel):
    ans = {symbol: np.zeros(len(data), dtype=np.int64) for symbol, data in panel.items()}
    if "MBT" not in panel:
        return ans
    data = panel["MBT"]
    close, seconds = data.close.to_numpy(), data.ct_sec.to_numpy()
    out = ans["MBT"]
    prior = None
    for session, positions in data.groupby("session", sort=False).indices.items():
        weekday = pd.Timestamp(session).dayofweek
        if weekday == 0 and prior is not None:
            start, end = prior
            side = -1 if end >= start else 1
            anchor = end
            for i in positions:
                if 61260 <= seconds[i] < 72000:
                    if side * (close[i] - anchor) <= -2500:
                        break
                    out[i] = side
        ref = [i for i in positions if 54000 <= seconds[i] <= 61200]
        prior = (close[ref[0]], close[ref[-1]]) if weekday == 4 and ref else None
    return ans


def entry_risk(panel):
    return {symbol: np.full(len(data), 250.0 if symbol == "MBT" else 0.0)
            for symbol, data in panel.items()}
