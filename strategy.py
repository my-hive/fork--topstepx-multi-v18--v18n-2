"""v18n-2 experiment 146.
FAMILY: gasoline_monday_asia_refinery_reversal
Mechanism: weekend refinery hedge positioning accumulated in thin Asia liquidity unwinds when
US refined-product liquidity returns.
Hypothesis: short RB Monday 17:00-06:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_monday_asia_refinery_reversal";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.items():
  if dow[ix[0]]!=0:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<21600]
  if not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if ref-c[i]<=-.006:stopped=True
   else:out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
