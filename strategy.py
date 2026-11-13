"""v18n-2 experiment 152.
FAMILY: copper_mediumterm_inventory_reversion
Mechanism: 20-session copper trend reflects inventory-hedging buildup that mean-reverts as physical
supply response catches up.
Hypothesis: fade completed 20-session HG direction at next reopen through US close; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="copper_mediumterm_inventory_reversion";PARAMS={"lookback_sessions":20,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];out=ans['HG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();moves=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if len(bars)>1:
   side=-np.sign(sum(moves[-20:])) if len(moves)>=20 else 0;moves.append(c[bars[-1]]-c[bars[0]])
   if not side:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.01:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HG' else 0.) for s,d in panel.items()}
