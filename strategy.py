"""v18n-2 experiment 84.
FAMILY: crude_us_opening_shock_reversal
Mechanism: extreme 08:30-09:30 crude moves exhaust opening liquidity; dealer inventory control
reverses move through settlement window.
Hypothesis: fade top-decile causal 08:30-09:30 CL shock from 09:31-15:00, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_us_opening_shock_reversal";PARAMS={"quantile":.9,"lookback_days":120,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];o=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby('session',sort=False).indices.values():
  b=[i for i in ix if 30600<=t[i]<34200];trade=[i for i in ix if 34260<=t[i]<54000]
  if b and trade and len(hist)>=PARAMS['lookback_days']:
   r=c[b[-1]]/c[b[0]]-1;th=np.quantile(np.abs(hist[-PARAMS['lookback_days']:]),PARAMS['quantile'])
   if abs(r)>th:
    side=-np.sign(r);ref=c[trade[0]]
    for i in trade:
     if side*(c[i]-ref)<=-.25:break
     o[i]=side
  if b:hist.append(c[b[-1]]/c[b[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='CL' else 0.) for s,d in panel.items()}
