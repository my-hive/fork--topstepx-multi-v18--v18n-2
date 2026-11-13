"""v18n-2 experiment 95.
FAMILY: gold_tuesday_us_session_reversal
Mechanism: Tuesday US-session gold price discovery reverses as physical and macro hedging
liquidity offsets early directional flow.
Hypothesis: short GC Tuesday 10:00-15:00 CT, $250 stop. Falsification: stressed PnL, era, or
yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_tuesday_us_session_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=1:continue
  bars=[i for i in ix if 36000<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if ref-c[i]<=-2.5:break
   o[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
