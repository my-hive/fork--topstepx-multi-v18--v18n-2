"""v18n-2 experiment 101.
FAMILY: yen_wednesday_us_session_reversal
Mechanism: Wednesday US risk-transfer demand reverses yen safe-haven positioning after early
Europe/Asia price discovery.
Hypothesis: short 6J Wednesday 08:30-15:00 CT, $250 stop. Falsification: stressed PnL, era, or
yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="yen_wednesday_us_session_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6J' not in panel:return ans
 d=panel['6J'];out=ans['6J'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=2:continue
  bars=[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref>=.00002:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='6J' else 0.) for s,d in panel.items()}
