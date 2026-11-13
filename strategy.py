"""v18n-2 experiment 93.
FAMILY: silver_wednesday_lunch_liquidity_reversal
Mechanism: Wednesday COMEX-morning silver shocks reverse when lunch liquidity lets commercial
hedgers absorb speculative flow.
Hypothesis: fade 08:30-11:30 SI move from 12:30-15:00 CT, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_wednesday_lunch_liquidity_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];o=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=2:continue
  pre=[i for i in ix if 30600<=t[i]<41400];bars=[i for i in ix if 45000<=t[i]<54000]
  if not pre or len(bars)<2:continue
  side=-np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars[1:]:
   if side*(c[i]-ref)<=-.5:break
   o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='SI' else 0.) for s,d in panel.items()}
