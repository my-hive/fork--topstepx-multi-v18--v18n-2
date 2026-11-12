"""v18n-2 experiment 13. Claimed family:
FAMILY: precious_metals_morning_extreme_continuation
Mechanism: completed 08:30->09:30 CT returns in top 2.5% of prior 300 sessions mark
major repricing days; correlated GC/SI afternoon follow-through reflects slower execution
of macro/hedging flows. Signal starts after 09:30, avoiding the 08:30-09:30 entry gate.
Hypothesis: independently trade GC/SI in direction of top-tail morning move 09:31->15:00,
one contract, $250 stop. Pre-screen: combined +$35.4k, 11/14 positive years, positive eras.
Falsification: stressed PnL/any era negative or fold result materially below pre-screen.
"""
import numpy as np

FAMILY = "precious_metals_morning_extreme_continuation"
PARAMS = {"quantile": 0.975, "lookback_sessions": 300, "entry_sec": 34260, "exit_sec": 54000, "stop_dollars": 250}
PV = {"GC": 100.0, "SI": 5000.0}


def _plan(df, pv):
    out = np.zeros(len(df), dtype=np.int64)
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    history = []
    for idx in df.groupby("session", sort=False).indices.values():
        opens = [i for i in idx if 30600 <= sec[i] < 30900]
        signal = [i for i in idx if 33900 <= sec[i] < 34200]
        entry = [i for i in idx if PARAMS["entry_sec"] <= sec[i] < PARAMS["exit_sec"]]
        if opens and signal:
            move = close[signal[-1]] / close[opens[0]] - 1
            past = np.abs(history[-PARAMS["lookback_sessions"]:])
            if len(past) >= PARAMS["lookback_sessions"]:
                if abs(move) >= np.quantile(past, PARAMS["quantile"]) and entry:
                    side, ref = int(np.sign(move)), close[entry[0]]
                    for i in entry:
                        if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / pv:
                            break
                        out[i] = side
            history.append(move)
    return out


def signals(panel):
    return {s: (_plan(d, PV[s]) if s in PV else np.zeros(len(d), dtype=np.int64)) for s, d in panel.items()}


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s in PV else 0.0) for s, d in panel.items()}
