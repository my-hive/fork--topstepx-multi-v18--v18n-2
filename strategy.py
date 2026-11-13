"""v18n-2 experiment 61.
FAMILY: gold_extreme_overnight_comex_continuation
Mechanism: extreme Asia/Europe gold repricing contains information that continues through COMEX
liquidity as macro hedgers complete execution.
Hypothesis: top-5% trailing-120-session overnight GC move trades same direction 08:30-15:00 CT,
$250 stop. Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
FAMILY="gold_extreme_overnight_comex_continuation";PARAMS={"quantile":.95,"lookback_sessions":120,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();days=list(d.groupby('session',sort=False).indices.values());hist=[]
 for ix in days:
  a=[i for i in ix if 61200<=t[i]<61500];b=[i for i in ix if 30600<=t[i]<30660];trade=[i for i in ix if 30660<=t[i]<54000]
  side=0
  if a and b and len(hist)>=120:
   r=c[b[0]]/c[a[0]]-1
   if abs(r)>=np.quantile(np.abs(hist[-120:]),.95):side=int(np.sign(r))
   hist.append(r)
  elif a and b:hist.append(c[b[0]]/c[a[0]]-1)
  if side and trade:
   ref=c[trade[0]]
   for i in trade:
    if side*(c[i]-ref)<=-2.5:break
    o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
