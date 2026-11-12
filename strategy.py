"""v18n-2 experiment 34. Claimed feed #3957.
FAMILY: gold_silver_ratio_extreme_reversion
Mechanism: an extreme completed GC/SI relative-value deviation reflects metal-specific
flow; substitutable precious-metal hedges rebalance it during following session.
Hypothesis: at prior session close, ratio z-score versus past 60 closes >=2: short GC/long
SI; <=-2: long GC/short SI, enter next 17:00 CT reopen through 15:00 CT. $250 stop per leg.
Falsification: stressed PnL/era negative or <70% positive years.
"""
import numpy as np

FAMILY = "gold_silver_ratio_extreme_reversion"
PARAMS = {"lookback_sessions": 60, "z_score": 2.0, "stop_dollars": 250}
PV = {"GC": 100.0, "SI": 5000.0}


def _session_groups(df):
    return list(df.groupby("session", sort=False).indices.values())


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if not {"GC", "SI"} <= set(panel):
        return ans
    gc, si = panel["GC"], panel["SI"]
    groups = {"GC": _session_groups(gc), "SI": _session_groups(si)}
    # Session labels match evaluator trading dates; intersect avoids a cross-holiday entry.
    ends = {}
    for sym, df in (("GC", gc), ("SI", si)):
        sec, close = df.ct_sec.to_numpy(), df.close.to_numpy()
        for idx in groups[sym]:
            bars = [i for i in idx if 53400 <= sec[i] <= 54000]
            if bars:
                ends.setdefault(sym, {})[df.session.iloc[idx[0]]] = close[bars[-1]]
    common = sorted(set(ends["GC"]) & set(ends["SI"]))
    pending = {}
    ratios = []
    for n, day in enumerate(common):
        ratio = ends["GC"][day] / ends["SI"][day]
        # Today's completed close creates an order only for next common session.
        if len(ratios) >= PARAMS["lookback_sessions"] and n + 1 < len(common):
            past = np.array(ratios[-PARAMS["lookback_sessions"]:])
            z = (ratio - past.mean()) / past.std(ddof=0) if past.std(ddof=0) else 0.0
            if abs(z) >= PARAMS["z_score"]:
                pending[common[n + 1]] = (-int(np.sign(z)), int(np.sign(z)))
        ratios.append(ratio)
    for sym, df in (("GC", gc), ("SI", si)):
        close, sec, out = df.close.to_numpy(), df.ct_sec.to_numpy(), ans[sym]
        ordered_days = [df.session.iloc[ix[0]] for ix in groups[sym]]
        for n, idx in enumerate(groups[sym]):
            side_tuple = pending.get(ordered_days[n])
            if not side_tuple:
                continue
            side = side_tuple[0] if sym == "GC" else side_tuple[1]
            bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
            if len(bars) < 2:
                continue
            ref = close[bars[0]]
            for i in bars[1:]:
                if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / PV[sym]:
                    break
                out[i] = side
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s in PV else 0.0) for s, d in panel.items()}
