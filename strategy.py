"""v18n-2 experiment 107.
FAMILY: crude_wednesday_inventory_followthrough
Mechanism: weekly inventory information causes afternoon crude repricing as physical supply
hedges complete after report release.
Hypothesis: follow 09:30-10:30 CL move from 11:00-15:00 Wednesday, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_wednesday_inventory_followthrough";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];out=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=2:continue
  pre=[i for i in ix if 34200<=t[i]<37800];bars=[i for i in ix if 39600<=t[i]<54000]
  if not pre or len(bars)<2:continue
  side=np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars[1:]:
   if side*(c[i]-ref)<=-.25:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
