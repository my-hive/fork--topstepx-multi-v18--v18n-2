"""v18n-2 experiment 141.
FAMILY: gold_monday_asia_safehaven_reversal
Mechanism: weekend safe-haven demand accumulated through Asia is unwound during US liquidity
normalization, producing a Monday overnight reversal in gold.
Hypothesis: short GC Monday 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_monday_asia_safehaven_reversal";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if dow[ix[0]]!=0:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if ref-c[i]<=-2.5:stopped=True
   else:out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
