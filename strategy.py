"""v18n-2 experiment 159.
FAMILY: heatingoil_friday_refinery_hedge_reversal
Mechanism: Friday refinery hedge flow follows the completed weekly energy move then mean-reverts
into US settlement as hedges are unwound.
Hypothesis: fade completed 5-session HO direction Friday 10:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="heatingoil_friday_refinery_hedge_reversal";PARAMS={"lookback_sessions":5,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HO' not in panel:return ans
 d=panel['HO'];out=ans['HO'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy();moves=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  x=[i for i in ix if 30600<=t[i]<34200];bars=[i for i in ix if 34260<=t[i]<54000]
  side=-np.sign(sum(moves[-5:])) if len(moves)>=5 and dow[ix[0]]==4 else 0
  if bars and side:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.006:break
    out[i]=side
  if len(x)>1:moves.append(c[x[-1]]-c[x[0]])
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HO' else 0.) for s,d in panel.items()}
