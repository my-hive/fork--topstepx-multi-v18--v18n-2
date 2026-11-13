"""v18n-2 experiment 99.
FAMILY: silver_tuesday_us_session_reversal
Mechanism: Tuesday US-session silver discovery reverses as industrial hedgers replenish liquidity.
Hypothesis: short SI 10:00-15:00 CT with exact $250 ($0.05) stop. Falsification: stressed PnL,
era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_tuesday_us_session_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=1:continue
  bars=[i for i in ix if 36000<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref>=.05: break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
