"""v18n-2 experiment 178.
FAMILY: gasoline_prior_us_shock_asia_reversal
Mechanism: an exceptional prior US RBOB move prompts overnight refinery/physical hedge adjustment
that reverses into Asian liquidity before next US open.
Hypothesis: fade top-decile prior US-session RB move 00:00-06:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_prior_us_shock_asia_reversal";PARAMS={"history_sessions":60,"quantile":.9,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();rets=[]
 for ix in d.groupby('session',sort=False).indices.values():
  us=np.array([i for i in ix if 30600<=t[i]<54000]);bars=[i for i in ix if t[i]<21600]
  prev=rets[-1] if rets else 0.;q=np.quantile(np.abs(rets[-61:-1]),.9) if len(rets)>=61 else np.inf;side=-np.sign(prev) if abs(prev)>=q else 0
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.006:break
    out[i]=side
  if len(us)>1:rets.append(c[us[-1]]-c[us[0]])
  else:rets.append(0.)
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
