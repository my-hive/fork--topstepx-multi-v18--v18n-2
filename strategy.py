"""v18n-2 experiment 8. Claimed independent seed-area family:
FAMILY: copper_sunday_reopen_long
Mechanism: COMEX copper's Sunday session includes first liquid price discovery after
weekend China/industrial-news accumulation. Development daily scan finds Sunday-session
HG mean +7.3bp (unlike its weak Monday/Tuesday), consistent with deferred reopening flow.
Hypothesis: long first available HG bar in Sunday-labelled session, hold through Monday
15:00 CT or a $250 completed-bar stop. One contract.
Falsification: stressed loss, negative era, or <70% positive years.
"""
import numpy as np
import pandas as pd

FAMILY = "copper_sunday_reopen_long"
PARAMS = {"exit_sec": 54000, "stop_dollars": 250}
HG_PV = 25000.0


def signals(panel):
    ans = {}
    for sym, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if sym == "HG":
            close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            for idx in df.groupby("session", sort=False).indices.values():
                # Session label is CT trading date. Sunday label starts 17:00 CT Sunday.
                session_day = pd.Timestamp(df.session.iloc[idx[0]]).day_of_week
                if session_day != 6:
                    continue
                ref = close[idx[0]]
                for i in idx[1:]:
                    if sec[i] >= PARAMS["exit_sec"] or close[i] - ref <= -PARAMS["stop_dollars"] / HG_PV:
                        break
                    out[i] = 1
        ans[sym] = out
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), PARAMS["stop_dollars"] if s == "HG" else 0.0)
            for s, d in panel.items()}
