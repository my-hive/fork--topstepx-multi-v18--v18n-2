"""v18n-2 experiment 98.
FAMILY: euro_monday_us_session_reversal
Mechanism: weekend euro positioning reverses in Monday US hours as US macro hedgers provide
liquidity after European price discovery.
Hypothesis: short M6E Monday 11:00-15:00 CT, $250 stop. Falsification: stressed PnL, era, or
yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="euro_monday_us_session_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'M6E' not in panel:return ans
 d=panel['M6E'];o=ans['M6E'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=0:continue
  bars=[i for i in ix if 39600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if ref-c[i]<=-.005:break
   o[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='M6E' else 0.) for s,d in panel.items()}
