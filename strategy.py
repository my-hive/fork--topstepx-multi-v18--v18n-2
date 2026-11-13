"""v18n-2 experiment 196.
FAMILY: euro_asia_silver_safehaven_reversal
Mechanism: Asian EUR move proxies global dollar risk; SI reverses that risk impulse at COMEX
liquidity as hedging shifts to US hours.
Hypothesis: fade completed 6E 06:00-08:30 direction in SI 08:30-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="euro_asia_silver_safehaven_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'6E','SI'}<=set(panel):return ans
 a=panel['6E'];d=panel['SI'];at=a.ct_sec.to_numpy();ac=a.close.to_numpy();sig={}
 for day,ix in a.groupby('session',sort=False).indices.items():
  x=[i for i in ix if 21600<=at[i]<30600]
  if len(x)>1:sig[pd.Timestamp(day)]=-np.sign(ac[x[-1]]-ac[x[0]])
 c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans['SI']
 for day,ix in d.groupby('session',sort=False).indices.items():
  side=sig.get(pd.Timestamp(day),0);bars=[i for i in ix if 30600<=t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
