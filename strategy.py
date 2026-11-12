"""v18n-2 experiment 21. Causal audit/correction of cross-asset family.
FAMILY: rates_prior_extreme_metals_continuation
Mechanism: top-tail completed ZN daily returns reveal durable macro rate repricing;
GC reacts with same-sign price flow during following session as global hedgers adjust.
Hypothesis: completed ZN T close signal enters 1 GC at T+1 17:00 CT reopen, exits T+1
15:00 CT, with $250 stop. Signal pending exactly one completed session; no same-session use.
Falsification: negative stressed PnL, negative era, or insufficient years.
"""
import numpy as np

FAMILY = "rates_prior_extreme_metals_continuation"
PARAMS = {"quantile": 0.95, "lookback_sessions": 300, "stop_dollars": 250}
GC_PV = 100.0


def _zn_sides(df):
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    prior, history, sides = None, [], []
    for idx in df.groupby("session", sort=False).indices.values():
        bars = [i for i in idx if 53400 <= sec[i] <= 54000]
        side = 0
        if bars and prior is not None:
            ret = close[bars[-1]] / prior - 1
            past = np.abs(history[-PARAMS["lookback_sessions"]:])
            if len(past) >= PARAMS["lookback_sessions"] and abs(ret) >= np.quantile(past, PARAMS["quantile"]):
                side = int(np.sign(ret))
            history.append(ret)
        if bars:
            prior = close[bars[-1]]
        sides.append(side)
    return sides


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if not {"GC", "ZN"} <= set(panel):
        return ans
    # Same ordered date set; shift preserves causality even when a holiday yields no entry.
    zn_sides = _zn_sides(panel["ZN"])
    df, out = panel["GC"], ans["GC"]
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    for n, idx in enumerate(df.groupby("session", sort=False).indices.values()):
        side = zn_sides[n - 1] if n and n - 1 < len(zn_sides) else 0
        bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
        if not side or len(bars) < 2:
            continue
        ref = close[bars[0]]
        for i in bars[1:]:
            if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / GC_PV:
                break
            out[i] = side
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "GC" else 0.0) for s, d in panel.items()}
