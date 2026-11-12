"""v18n-2 experiment 12. Claimed metals pivot family:
FAMILY: gold_midday_extreme_continuation
Mechanism: a US-session gold move that reaches >=95th percentile of its trailing 300
session distribution by 11:30 CT signals durable macro repricing rather than ordinary
noise; afternoon flow continues it. Only extreme top-tail moves are used, not normal days.
Hypothesis: from first bar after 11:30 CT through 15:00 CT, trade direction of the
completed 08:30->11:30 GC return if |return| >= 0.95 quantile of trailing 300 sessions.
$250 stop, 1 contract. Causal quantile uses only past completed sessions.
Falsification: negative stressed PnL/any era, <70% years, or flat fold outcome.
"""
import numpy as np

FAMILY = "gold_midday_extreme_continuation"
PARAMS = {
    "quantile": 0.95,
    "lookback_sessions": 300,
    "entry_sec": 41460,
    "exit_sec": 54000,
    "stop_dollars": 250,
}
GC_PV = 100.0


def signals(panel):
    ans = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "GC":
            close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            history = []
            for idx in df.groupby("session", sort=False).indices.values():
                opens = [i for i in idx if 30600 <= sec[i] < 30900]
                signals_ = [i for i in idx if 41100 <= sec[i] < 41400]
                entry = [i for i in idx if PARAMS["entry_sec"] <= sec[i] < PARAMS["exit_sec"]]
                if opens and signals_:
                    move = close[signals_[-1]] / close[opens[0]] - 1
                    past = np.abs(history[-PARAMS["lookback_sessions"]:])
                    if len(past) >= PARAMS["lookback_sessions"]:
                        threshold = np.quantile(past, PARAMS["quantile"])
                        if abs(move) >= threshold and entry:
                            side, ref = int(np.sign(move)), close[entry[0]]
                            for i in entry:
                                if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / GC_PV:
                                    break
                                out[i] = side
                    history.append(move)
        ans[sym] = out
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "GC" else 0.0) for s, d in panel.items()}
