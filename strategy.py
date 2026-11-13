"""v18n-2 experiment 109.
FAMILY: thirtyyear_thursday_auction_reversal
Mechanism: Thursday long-bond auction allocation briefly dislocates prices; dealer balance-sheet
rebalancing reverses initial post-auction move.
Hypothesis: fade ZB 12:00-12:30 move through 15:00 CT Thursday, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="thirtyyear_thursday_auction_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel:return ans
 d=panel['ZB'];out=ans['ZB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=3:continue
  pre=[i for i in ix if 43200<=t[i]<45000];bars=[i for i in ix if 45000<=t[i]<54000]
  if not pre or len(bars)<2:continue
  side=-np.sign(c[pre[-1]]-c[pre[0]]);ref=c[bars[0]]
  for i in bars[1:]:
   if side*(c[i]-ref)<=-.25:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZB' else 0.) for s,d in panel.items()}
