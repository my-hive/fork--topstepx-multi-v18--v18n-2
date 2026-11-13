"""v18n-2 experiment 219.
FAMILY: crude_prior_session_refinery_reversal
Mechanism: prior-session refinery hedging pressure reverses as next-session physical liquidity
rebalances crude exposure.
Hypothesis: fade completed prior CL US-session direction through next US session; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_prior_session_refinery_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();prev=0.
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000];side=-np.sign(prev)
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.25:break
    out[i]=side
  if len(bars)>1:prev=c[bars[-1]]-c[bars[0]]
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
