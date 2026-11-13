"""v18n-2 experiment 52.
FAMILY: nasdaq_monday_weekend_risk_premium
Mechanism: weekend information release and systematic Monday allocation create persistent
Nasdaq futures risk premium through Monday US close.
Hypothesis: long NQ Monday 17:00 CT reopen through 15:00 CT, $250 stop. Falsification:
stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="nasdaq_monday_weekend_risk_premium";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];o=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=0:continue
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref<=-12.5:break
   o[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='NQ' else 0.) for s,d in panel.items()}
