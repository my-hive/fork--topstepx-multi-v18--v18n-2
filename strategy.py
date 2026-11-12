"""v18n-2 experiment 17. Causal correction to exp15, separately recorded.
FAMILY: silver_daily_extreme_close_continuation
Mechanism: extreme completed SI daily close-to-close return indicates macro repricing.
Only after close is known, next trading session's 17:00 CT reopen may continue flow.
Hypothesis: signal formed at session T close, enter direction at session T+1 reopen,
hold through T+1 15:00, $250 stop. No current-session backfill is permitted.
Falsification: any stressed loss/negative era or weak year coverage.
"""
import numpy as np

FAMILY = "silver_daily_extreme_close_continuation"
PARAMS = {"quantile": 0.95, "lookback_sessions": 300, "stop_dollars": 250}
SI_PV = 5000.0


def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "SI" not in panel:
        return ans
    df, out = panel["SI"], ans["SI"]
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    prior_close, history, pending = None, [], 0
    for idx in df.groupby("session", sort=False).indices.values():
        # pending arose from prior completed session; valid from this session's reopen.
        bars = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < 54000]
        if pending and len(bars) > 1:
            ref = close[bars[0]]
            for i in bars[1:]:
                if pending * (close[i] - ref) <= -PARAMS["stop_dollars"] / SI_PV:
                    break
                out[i] = pending
        pending = 0
        close_bars = [i for i in idx if 53400 <= sec[i] <= 54000]
        if not close_bars:
            continue
        session_close = close[close_bars[-1]]
        if prior_close is not None:
            move = session_close / prior_close - 1
            past = np.abs(history[-PARAMS["lookback_sessions"]:])
            if len(past) >= PARAMS["lookback_sessions"] and abs(move) >= np.quantile(past, PARAMS["quantile"]):
                pending = int(np.sign(move))
            history.append(move)
        prior_close = session_close
    return ans


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s == "SI" else 0.0) for s, d in panel.items()}
