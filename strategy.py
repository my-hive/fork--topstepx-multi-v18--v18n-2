"""v18n-2 experiment 73.
FAMILY: yen_tuesday_safehaven_reversal
Mechanism: Tuesday Japanese-yen dealer inventory reverses after Asia-session safe-haven demand
is met by US corporate and macro hedging flow.
Hypothesis: short 6J Tuesday 17:00 CT through 15:00 CT, $250 stop. Falsification: stressed PnL,
era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="yen_tuesday_safehaven_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6J' not in panel:return ans
 d=panel['6J'];o=ans['6J'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=1:continue
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if ref-c[i]<=-.00002:break
   o[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='6J' else 0.) for s,d in panel.items()}
