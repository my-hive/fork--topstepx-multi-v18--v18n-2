"""v18n-2 experiment 23. Claimed feed #3911.
FAMILY: silver_morning_volume_anomaly_continuation
Mechanism: an abnormal completed 08:30-09:30 CT SI volume hour identifies information
arrival or institutional flow. Its price direction continues as remaining execution occurs.
Hypothesis: if hour volume is top 5% of prior 60 sessions, trade its direction 09:31->15:00,
$250 stop. All signal bars complete before entry. Falsification: stressed PnL/era negative.
"""
import numpy as np

FAMILY = "silver_morning_volume_anomaly_continuation"
PARAMS = {"quantile": 0.95, "lookback_sessions": 60, "entry_sec": 34260, "exit_sec": 54000, "stop_dollars": 250}
SI_PV = 5000.0


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "SI" not in panel:
        return ans
    df, out = panel["SI"], ans["SI"]
    close, vol, sec = df.close.to_numpy(), df.volume.to_numpy(), df.ct_sec.to_numpy()
    history = []
    for idx in df.groupby("session", sort=False).indices.values():
        hour = [i for i in idx if 30600 <= sec[i] < 34200]
        entry = [i for i in idx if PARAMS["entry_sec"] <= sec[i] < PARAMS["exit_sec"]]
        if not hour:
            continue
        volume = vol[hour].sum()
        past = history[-PARAMS["lookback_sessions"]:]
        if len(past) >= PARAMS["lookback_sessions"] and volume >= np.quantile(past, PARAMS["quantile"]) and entry:
            side, ref = int(np.sign(close[hour[-1]] - close[hour[0]])), close[entry[0]]
            for i in entry:
                if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / SI_PV:
                    break
                out[i] = side
        history.append(volume)
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "SI" else 0.0) for s, d in panel.items()}
