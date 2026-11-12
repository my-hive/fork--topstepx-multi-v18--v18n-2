"""v18n-2 experiment 22. Claimed feed #8058.
FAMILY: silver_stalled_trend_reversal
Mechanism: an extreme completed daily SI move that is followed by a near-flat session
indicates repricing failed to attract continuation; next-session position unwinds reverse it.
Hypothesis: after an SI top-5% daily move followed by a session whose absolute return is
less than 10% of initial move, enter opposite stalled-day direction at following 17:00 CT
reopen; exit 15:00 CT; $250 stop. All state comes from completed sessions.
Falsification: negative stressed PnL/any era or inadequate positive years.
"""
import numpy as np

FAMILY = "silver_stalled_trend_reversal"
PARAMS = {"quantile": 0.95, "lookback_sessions": 300, "stall_ratio": 0.10, "stop_dollars": 250}
SI_PV = 5000.0


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "SI" not in panel:
        return ans
    df, out = panel["SI"], ans["SI"]
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    prior_close, history, candidate, pending = None, [], 0.0, 0
    for idx in df.groupby("session", sort=False).indices.values():
        bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
        if pending and len(bars) > 1:
            ref = close[bars[0]]
            for i in bars[1:]:
                if pending * (close[i] - ref) <= -PARAMS["stop_dollars"] / SI_PV:
                    break
                out[i] = pending
        pending = 0
        end = [i for i in idx if 53400 <= sec[i] <= 54000]
        if not end:
            continue
        this_close = close[end[-1]]
        if prior_close is not None:
            ret = this_close / prior_close - 1
            # Candidate was established at prior completed close. This close confirms stall.
            if candidate and abs(ret) < PARAMS["stall_ratio"] * abs(candidate):
                pending = -int(np.sign(candidate))
            past = np.abs(history[-PARAMS["lookback_sessions"]:])
            candidate = ret if len(past) >= PARAMS["lookback_sessions"] and abs(ret) >= np.quantile(past, PARAMS["quantile"]) else 0.0
            history.append(ret)
        prior_close = this_close
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "SI" else 0.0) for s, d in panel.items()}
