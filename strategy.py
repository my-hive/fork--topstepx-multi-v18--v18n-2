"""v18n-2 experiment 1.
FAMILY: metals_us_opening_overnight_unwind
Mechanism: thin Asian/London gold move can be liquidity-driven; deeper COMEX opening
liquidity should unwind an extreme overnight move.
Hypothesis: reverse completed 60-minute pre-open GC return from 08:30 through 09:29 CT.
Falsification: stressed PnL lacks positive support across chronological eras or <70% positive years.
"""
import numpy as np

FAMILY = "metals_us_opening_overnight_unwind"
PARAMS = {"lookback_minutes": 60}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol != "GC":
            result[symbol] = out
            continue
        close = df.close.to_numpy()
        sec = df.ct_sec.to_numpy()
        for indices in df.groupby("session", sort=False).indices.values():
            for j in range(PARAMS["lookback_minutes"], len(indices)):
                i = indices[j]
                if 30600 <= sec[i] < 34200:
                    out[i] = -int(np.sign(close[i] - close[indices[j - PARAMS["lookback_minutes"]]]))
        result[symbol] = out
    return result


def entry_risk(panel):
    return {symbol: np.full(len(df), 300.0 if symbol == "GC" else 0.0) for symbol, df in panel.items()}
