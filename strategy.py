"""v18n-2 experiment 153.
FAMILY: copper_quiet_regime_inventory_followthrough
Mechanism: when recent copper volatility is suppressed, prior inventory-hedging direction persists
into the next physical session instead of exhausting in a high-volatility repricing.
Hypothesis: follow prior HG sign after low 20-session realized volatility, 17:00-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="copper_quiet_regime_inventory_followthrough";PARAMS={"volatility_lookback":20,"regime_history":60,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];out=ans['HG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();moves=[];vols=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if len(bars)>1:
   move=c[bars[-1]]-c[bars[0]];vol=np.std(moves[-20:]) if len(moves)>=20 else np.inf;th=np.quantile(vols[-60:],.2) if len(vols)>=60 else -np.inf
   side=np.sign(moves[-1]) if vol<th and moves else 0;moves.append(move);vols.append(vol)
   if not side:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.01:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HG' else 0.) for s,d in panel.items()}
