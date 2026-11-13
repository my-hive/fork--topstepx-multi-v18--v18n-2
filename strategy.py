"""v18n-2 experiment 155.
FAMILY: copper_monday_weekend_inventory_reversal
Mechanism: weekend physical-inventory order imbalances extend a short copper trend into Monday,
then reverse as US warehouse and hedging liquidity returns.
Hypothesis: fade completed 10-session HG direction Monday, 17:00-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="copper_monday_weekend_inventory_reversal";PARAMS={"lookback_sessions":10,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];out=ans['HG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();moves=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if len(bars)>1:
   side=-np.sign(sum(moves[-10:])) if len(moves)>=10 and dow[ix[0]]==0 else 0;moves.append(c[bars[-1]]-c[bars[0]])
   if not side:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.01:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HG' else 0.) for s,d in panel.items()}
