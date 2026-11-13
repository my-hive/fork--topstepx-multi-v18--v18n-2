"""v18n-2 experiment 221.
FAMILY: spx_monthend_closing_auction_reversal
Mechanism: institutional month-end closing-auction demand reverses next US session as passive
rebalance orders complete.
Hypothesis: fade completed prior final-three-session ES direction during next US session; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="spx_monthend_closing_auction_reversal";PARAMS={"window_sessions":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ES' not in panel:return ans
 d=panel['ES'];out=ans['ES'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);prev=0.
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000];side=-np.sign(prev)
  if side and bars:
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-5:break
    out[i]=side
  us=[i for i in ix if 30600<=t[i]<54000]
  if len(us)>1 and dt.iloc[ix[0]].day>=26:prev=c[us[-1]]-c[us[0]]
  else:prev=0.
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
