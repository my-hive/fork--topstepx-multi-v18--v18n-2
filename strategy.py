"""v18n-2 experiment 2 (exp 1 churned per-minute; logged as failed).
FAMILY: metals_us_opening_overnight_unwind
Mechanism: thin Asia/London gold moves are partly liquidity-driven; deep COMEX open liquidity unwinds them.
Hypothesis: fade completed prior-60min MGC move once at 08:30 CT, hold to 11:00 CT, vol stop, risk-sized.
Falsification: stressed PnL not positive in all 3 eras or <70% positive years.
"""
import numpy as np

FAMILY = "metals_us_opening_overnight_unwind"
PARAMS = {"lookback_min": 60, "vol_window": 240, "stop_vol_mult": 1.0, "exit_ct_sec": 39600, "risk_budget": 280}
SYM = "MGC"
PV = 10.0
ENTRY_SEC = 30600  # 08:30 CT


def _plan(df):
    """Per-row desired target and per-contract risk, causal."""
    n = len(df)
    out = np.zeros(n, dtype=np.int64)
    risk = np.zeros(n)
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    lb, vw = PARAMS["lookback_min"], PARAMS["vol_window"]
    for idx in df.groupby("session", sort=False).indices.values():
        c, s = close[idx], sec[idx]
        # first bar at/after entry time, if bar present within 5 minutes
        hits = np.nonzero((s >= ENTRY_SEC) & (s < ENTRY_SEC + 300))[0]
        if not len(hits) or hits[0] < max(lb, vw):
            continue
        j = hits[0]
        move = c[j] - c[j - lb]
        r = np.diff(c[j - vw:j + 1])
        stop = PARAMS["stop_vol_mult"] * r.std() * np.sqrt(lb)
        per = stop * PV + 2.0  # + slippage buffer
        n_c = int(min(50, PARAMS["risk_budget"] // per))
        if move == 0 or n_c < 1 or stop <= 0:
            continue
        side = -int(np.sign(move))
        ref, pos = c[j], 0
        for k in range(j, len(idx)):
            if s[k] >= PARAMS["exit_ct_sec"]:
                break
            if k > j and side * (c[k] - ref) <= -stop:
                break
            out[idx[k]] = side * n_c
            risk[idx[k]] = per
    return out, risk


def signals(panel):
    return {s: (_plan(d)[0] if s == SYM else np.zeros(len(d), dtype=np.int64)) for s, d in panel.items()}


def entry_risk(panel):
    return {s: (_plan(d)[1] if s == SYM else np.zeros(len(d))) for s, d in panel.items()}
