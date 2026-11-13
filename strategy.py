"""v18n-2 experiment 207.
FAMILY: yen_heatingoil_prior_us_macro_reversal_causal_repair
Mechanism: prior US yen risk move reflects dollar funding demand that reverses heating-oil Asia
hedges before refinery liquidity opens.
Hypothesis: fade completed prior 6J US direction in HO 00:00-08:30; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="yen_heatingoil_prior_us_macro_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'6J','HO'}<=set(panel):return ans
 a=panel['6J'];at=a.ct_sec.to_numpy();ac=a.close.to_numpy();prev={}
 for day,ix in a.groupby('session',sort=False).indices.items():
  x=[i for i in ix if 30600<=at[i]<54000]
  if len(x)>1:prev[pd.Timestamp(day)]=ac[x[-1]]-ac[x[0]]
 signal={pd.Timestamp(day)+pd.offsets.BDay(1):-np.sign(v) for day,v in prev.items()}
 d=panel['HO'];out=ans['HO'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for day,ix in d.groupby('session',sort=False).indices.items():
  side=signal.get(pd.Timestamp(day),0);bars=[i for i in ix if t[i]<30600]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.006:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HO' else 0.) for s,d in panel.items()}
