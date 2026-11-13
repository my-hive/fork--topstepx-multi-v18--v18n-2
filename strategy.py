"""v18n-2 experiment 102.
FAMILY: soybeans_thursday_us_session_reversal
Mechanism: Thursday soybean US-session moves reverse as commercial crop hedgers offset early
speculative positioning.
Hypothesis: short ZS Thursday 08:30-13:30 CT, $250 stop. Falsification: stressed PnL, era, or
yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="soybeans_thursday_us_session_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZS' not in panel:return ans
 d=panel['ZS'];out=ans['ZS'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=3:continue
  bars=[i for i in ix if 30600<=t[i]<49200]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref>=5.:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZS' else 0.) for s,d in panel.items()}
