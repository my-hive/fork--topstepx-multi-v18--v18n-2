"""v18n-2 experiment 33.
FAMILY: copper_prior_high_volume_continuation
Mechanism: a high-volume copper session reflects industrial information arrival and hedger
flow; next-session price adjustment continues in the same direction.
Hypothesis: prior HG session volume top 5% vs trailing 60 and directional session return;
enter same direction at next 17:00 CT reopen and exit 15:00 CT, $250 stop.
Falsification: stressed PnL/era negative or poor year coverage.
"""
import numpy as np

FAMILY = "copper_prior_high_volume_continuation"
PARAMS = {"quantile": 0.95, "lookback_sessions": 60, "stop_dollars": 250}
HG_PV = 25000.0


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "HG" not in panel:
        return ans
    df, out = panel["HG"], ans["HG"]
    close, vol, sec = df.close.to_numpy(), df.volume.to_numpy(), df.ct_sec.to_numpy()
    volume_history, pending = [], 0
    for idx in df.groupby("session", sort=False).indices.values():
        bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
        if pending and len(bars) > 1:
            ref = close[bars[0]]
            for i in bars[1:]:
                if pending * (close[i] - ref) <= -PARAMS["stop_dollars"] / HG_PV:
                    break
                out[i] = pending
        pending = 0
        full = list(idx)
        end = [i for i in idx if 53400 <= sec[i] <= 54000]
        if not full or not end:
            continue
        session_volume = vol[full].sum()
        past = volume_history[-PARAMS["lookback_sessions"]:]
        # Entire session now complete; trade cannot start until next session.
        if len(past) >= PARAMS["lookback_sessions"] and session_volume >= np.quantile(past, PARAMS["quantile"]):
            pending = int(np.sign(close[end[-1]] - close[full[0]]))
        volume_history.append(session_volume)
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "HG" else 0.0) for s, d in panel.items()}
