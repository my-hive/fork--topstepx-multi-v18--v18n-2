"""v18n-2 experiment 41.
FAMILY: gold_prior_high_range_continuation
Mechanism: a high-range gold session indicates durable macro information arrival; next-day
same-direction exposure captures gradual repricing, conditioned on prior range top quintile.
Hypothesis: prior completed GC range top 20% trailing 60 sessions; follow prior direction
next reopen to 15:00 CT, $250 stop. Falsification: stress/era/year failure.
"""
import numpy as np
FAMILY="gold_prior_high_range_continuation";PARAMS={"quantile":.8,"lookback_sessions":60,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy();hist=[];pending=0
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if pending and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if pending*(c[i]-ref)<=-2.5:break
    o[i]=pending
  pending=0;end=[i for i in ix if 53400<=t[i]<=54000]
  if not end:continue
  r=(h[ix].max()-l[ix].min())/c[ix[0]];past=hist[-60:]
  if len(past)>=60 and r>=np.quantile(past,.8):pending=int(np.sign(c[end[-1]]-c[ix[0]]))
  hist.append(r)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
