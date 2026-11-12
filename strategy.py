"""v18n-2 experiment 7. Claimed independent family:
FAMILY: gold_silver_daily_divergence_reversion
Mechanism: GC and SI share monetary-metal macro beta. A prior-session relative-return
divergence is often transient liquidity/positioning, so relative loser catches up during
following liquid US hours; market-neutral pair limits dollar-beta exposure.
Hypothesis: at 08:30 CT, long prior-day loser and short prior-day winner in GC/SI;
hold through 15:00 CT, no threshold or parameter-selected entry.
Falsification: negative stressed total/era PnL or <70% positive years.
"""
import numpy as np
import pandas as pd

FAMILY = "gold_silver_daily_divergence_reversion"
PARAMS = {"entry_sec": 30600, "exit_sec": 54000}


def signals(panel):
    res = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if not {"GC", "SI"} <= set(panel):
        return res
    g, z = panel["GC"], panel["SI"]
    # Build only from each prior completed session's final close.
    gc = g.groupby("session", sort=False).close.last()
    sc = z.groupby("session", sort=False).close.last()
    common = gc.index.intersection(sc.index)
    gr, sr = gc.loc[common].pct_change(), sc.loc[common].pct_change()
    side = np.sign(gr - sr).shift(1)  # positive: GC outperformed yesterday, short GC today
    sides = dict(zip(pd.DatetimeIndex(common).strftime("%Y-%m-%d"), side.fillna(0).astype(int)))
    for sym, df in (("GC", g), ("SI", z)):
        out = res[sym]
        sec = df.ct_sec.to_numpy()
        for idx in df.groupby("session", sort=False).indices.values():
            signal = sides.get(pd.Timestamp(df.session.iloc[idx[0]]).strftime("%Y-%m-%d"), 0)
            for i in idx:
                if PARAMS["entry_sec"] <= sec[i] < PARAMS["exit_sec"]:
                    out[i] = -signal if sym == "GC" else signal
    return res


def entry_risk(panel):
    # Pair's opposite legs hedge common metal beta; conservative $250/leg loss bound.
    return {s: np.full(len(d), 250.0 if s in {"GC", "SI"} else 0.0) for s, d in panel.items()}
