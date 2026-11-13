"""v18n-2 experiment 51.
FAMILY: gasoline_friday_driving_demand
Mechanism: Friday refined-product demand hedging ahead of weekend driving creates a positive
RBOB risk premium into US close.
Hypothesis: long RB Friday from 17:00 CT reopen through 15:00 CT, $250 completed-bar stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_friday_driving_demand";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];o=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=4:continue
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref<=-250/42000:break
   o[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='RB' else 0.) for s,d in panel.items()}
