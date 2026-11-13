"""v18n-2 experiment 79.
FAMILY: heatingoil_monday_priorloss_hedging_reversal
Mechanism: after prior-session losses, Monday physical distributor hedging reverses residual
opening inventory positioning once US desks arrive.
Hypothesis: short HO Monday 10:00-15:00 CT only after prior HO session loss, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="heatingoil_monday_priorloss_hedging_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HO' not in panel:return ans
 d=panel['HO'];o=ans['HO'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();days=list(d.groupby('session',sort=False).indices.values());rets=[]
 for n,ix in enumerate(days):
  side=pd.Timestamp(d.session.iloc[ix[0]]).dayofweek==0 and n and rets[-1]<0
  bars=[i for i in ix if 36000<=t[i]<54000]
  if side and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if ref-c[i]<=-.006:break
    o[i]=-1
  rets.append(c[ix[-1]]/c[ix[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='HO' else 0.) for s,d in panel.items()}
