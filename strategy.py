"""v18n-2 experiment 35. Diagnostic of FAMILY metals_extreme_overnight_continuation.
Mechanism unchanged: unusually large completed overnight SI move indicates information
arrival whose direction persists after COMEX opens. This is a declared threshold-definition
audit after exp10 used median-relative move.
Hypothesis: SI overnight absolute return >= causal 95th percentile of trailing 300 overnight
returns; trade direction 08:30->15:00, $250 stop. Falsification: stressed PnL/era failure.
"""
import numpy as np
FAMILY="metals_extreme_overnight_continuation"
PARAMS={"quantile":.95,"lookback_sessions":300,"entry_sec":30600,"exit_sec":54000,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "SI" not in panel:return ans
 d=panel["SI"];o=ans["SI"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby("session",sort=False).indices.values():
  pre=[i for i in ix if t[i]>=61200 or t[i]<30600];e=[i for i in ix if PARAMS["entry_sec"]<=t[i]<PARAMS["exit_sec"]]
  if len(pre)<2:continue
  r=c[pre[-1]]/c[pre[0]]-1;past=np.abs(hist[-PARAMS["lookback_sessions"]:])
  if len(past)>=PARAMS["lookback_sessions"] and abs(r)>=np.quantile(past,PARAMS["quantile"]) and e:
   side,ref=int(np.sign(r)),c[e[0]]
   for i in e:
    if side*(c[i]-ref)<=-PARAMS["stop_dollars"]/5000:break
    o[i]=side
  hist.append(r)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=="SI" else 0.) for s,d in panel.items()}
