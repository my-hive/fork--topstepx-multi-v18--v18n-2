"""v18n-2 experiment 11. Independent metals family.
FAMILY: silver_extreme_reopen_gap_continuation
Mechanism: extreme SI price gap from prior US close to 17:00 CT reopen reflects discrete
macro/FX news while COMEX is shut; reopening participants continue repricing during next
US session. Unlike overnight drift, this is a closed-market discontinuity.
Hypothesis: SI gap magnitude >=5x trailing 60-session median gap, enter direction at
09:35 CT, one contract, $250 stop, flat 15:00 CT. Pre-screen: 195 events, +$201 net/event,
10/14 positive years. Falsification: stressed PnL/era failure or weak fold outcome.
"""
import numpy as np

FAMILY = "silver_extreme_reopen_gap_continuation"
PARAMS = {"z_min": 5.0, "vol_sessions": 60, "entry_sec": 34500, "exit_sec": 54000, "stop_dollars": 250}
SI_PV = 5000.0


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "SI" not in panel:
        return ans
    df = panel["SI"]
    out = ans["SI"]
    c, s = df.close.to_numpy(), df.ct_sec.to_numpy()
    gaps = []
    prior_close = None
    for idx in df.groupby("session", sort=False).indices.values():
        reopen = [i for i in idx if 61200 <= s[i] < 61500]
        us_close = [i for i in idx if 53700 <= s[i] <= 54000]
        entry = [i for i in idx if PARAMS["entry_sec"] <= s[i] < PARAMS["exit_sec"]]
        if not reopen or prior_close is None:
            if us_close:
                prior_close = c[us_close[-1]]
            continue
        gap = c[reopen[0]] / prior_close - 1
        past = gaps[-PARAMS["vol_sessions"]:]
        gaps.append(abs(gap))
        if us_close:
            next_prior = c[us_close[-1]]
        else:
            next_prior = prior_close
        if len(past) >= PARAMS["vol_sessions"] and entry and abs(gap) >= PARAMS["z_min"] * np.median(past):
            side, ref = int(np.sign(gap)), c[entry[0]]
            for i in entry:
                if side * (c[i] - ref) <= -PARAMS["stop_dollars"] / SI_PV:
                    break
                out[i] = side
        prior_close = next_prior
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "SI" else 0.0) for s, d in panel.items()}
