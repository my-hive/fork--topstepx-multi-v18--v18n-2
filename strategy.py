"""v18n-2 experiment 42.
FAMILY: gold_prior_low_volume_trend_continuation
Mechanism: a directional gold session on unusually low volume can signal persistent central
bank/slow allocator demand rather than an exhausted speculative shock; next session extends.
Hypothesis: completed GC volume bottom quintile versus prior 60 sessions and directional
close; follow direction next reopen to 15:00 CT. $250 stop. Falsification: stress/era/years.
"""
import numpy as np
FAMILY="gold_prior_low_volume_trend_continuation";PARAMS={"quantile":.2,"lookback_sessions":60,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,v,t=d.close.to_numpy(),d.volume.to_numpy(),d.ct_sec.to_numpy();hist=[];pending=0
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if pending and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if pending*(c[i]-ref)<=-2.5:break
    o[i]=pending
  pending=0;end=[i for i in ix if 53400<=t[i]<=54000]
  if not end:continue
  volume=v[ix].sum();past=hist[-60:]
  if len(past)>=60 and volume<=np.quantile(past,.2):pending=int(np.sign(c[end[-1]]-c[ix[0]]))
  hist.append(volume)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
