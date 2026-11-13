"""v18n-2 experiment 180.
FAMILY: copper_prior_settlement_asia_continuation
Mechanism: previous session COMEX late-settlement industrial hedge direction persists into following
Asian base-metal liquidity.
Hypothesis: follow prior completed 15:00-17:00 HG move next session 00:00-04:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="copper_prior_settlement_asia_continuation";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];out=ans['HG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();prior=0.
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if t[i]<14400];side=np.sign(prior)
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.01:break
    out[i]=side
  x=[i for i in ix if 54000<=t[i]<61200]
  prior=c[x[-1]]-c[x[0]] if len(x)>1 else 0.
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HG' else 0.) for s,d in panel.items()}
