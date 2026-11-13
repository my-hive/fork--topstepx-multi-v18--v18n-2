"""v18n-2 experiment 60.
FAMILY: gold_quiet_session_reversal
Mechanism: low-range gold sessions reflect temporary liquidity imbalance rather than information;
following-session reversal captures dealer inventory normalization.
Hypothesis: after completed bottom-decile 120-session absolute GC return, trade opposite direction
next 17:00 CT through 15:00 CT, $250 stop. Falsification: stressed PnL, era, or year failure.
"""
import numpy as np
FAMILY="gold_quiet_session_reversal";PARAMS={"quantile":.1,"lookback_sessions":120,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();days=list(d.groupby('session',sort=False).indices.values());rets=[]
 for n,ix in enumerate(days):
  side=0
  if n and len(rets)>=120:
   r=rets[-1]
   if abs(r)<=np.quantile(np.abs(rets[-120:]),.1):side=-int(np.sign(r))
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if side and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if side*(c[i]-ref)<=-2.5:break
    o[i]=side
  rets.append(c[ix[-1]]/c[ix[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
