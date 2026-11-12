"""v18n-2 experiment 16. Independent cross-metal/rates family:
FAMILY: rates_extreme_move_metals_continuation
Mechanism: extreme completed daily moves in 10-year Treasury-note futures (top 5% vs
trailing 300 sessions) signal durable macro repricing in real yields. Gold and silver
respond directionally with yields; metals continue after the rate close because their
positioning adjusts during the next session.
Hypothesis: on extreme prior-session ZN return, trade GC and SI in the sign of that
ZN return from the metals session close through the next close, $250 stop per contract.
Causal rolling quantile only. Falsification: stressed PnL or era failure.
"""
import numpy as np
import pandas as pd

FAMILY = "rates_extreme_move_metals_continuation"
PARAMS = {"quantile": 0.95, "lookback_sessions": 300, "stop_dollars": 250}
PV = {"GC": 100.0, "SI": 5000.0}
CLOSE_LO, CLOSE_HI = 53400, 54000


def _zn_extremes(zn):
    close = zn[zn.ct_sec.between(CLOSE_LO, CLOSE_HI)].groupby("session").close.last()
    ret = close.pct_change()
    past = ret.abs().shift(1)
    threshold = past.rolling(PARAMS["lookback_sessions"], min_periods=PARAMS["lookback_sessions"]).quantile(PARAMS["quantile"])
    active = ret.abs() >= threshold
    dates = pd.DatetimeIndex(ret.index[active.fillna(False)])
    return dict(zip(dates.strftime("%Y-%m-%d"), np.sign(ret.loc[dates]).astype(int)))


def _plan(df, pv, zn_sides):
    out = np.zeros(len(df), dtype=np.int64)
    close, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
    for idx in df.groupby("session", sort=False).indices.values():
        # Prior metal session's ZN signal is complete before this metal session starts.
        key = pd.Timestamp(df.session.iloc[idx[0]]).strftime("%Y-%m-%d")
        side = zn_sides.get(key, 0)
        if side == 0:
            continue
        next_session = [i for i in idx if 61200 <= sec[i] < 61500] + [i for i in idx if 30600 <= sec[i] < CLOSE_LO]
        bars = next_session
        if len(bars) < 2:
            continue
        ref = close[bars[0]]
        for i in bars[1:]:
            if side * (close[i] - ref) <= -PARAMS["stop_dollars"] / pv:
                break
            out[i] = side
    return out


def signals(panel):
    zn_sides = _zn_extremes(panel["ZN"]) if "ZN" in panel else {}
    return {s: (_plan(d, PV[s], zn_sides) if s in PV else np.zeros(len(d), dtype=np.int64))
            for s, d in panel.items()}


def entry_risk(panel):
    return {s: np.full(len(d), 290.0 if s in PV else 0.0) for s, d in panel.items()}
