"""v18n-2 experiment 176.
FAMILY: naturalgas_june_storage_hedge_reversal
Mechanism: June early US storage/utility hedging moves in the first cash half-hour reverse as
physical liquidity absorbs the pressure by 11:00.
Hypothesis: fade completed 08:30-09:00 NG move in June through 11:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="naturalgas_june_storage_hedge_reversal";PARAMS={"month":6,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NG' not in panel:return ans
 d=panel['NG'];out=ans['NG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mo=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 30600<=t[i]<32400];bars=[i for i in ix if 32400<=t[i]<39600]
  if mo[ix[0]]!=6 or len(x)<2 or not bars:continue
  side=-np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.025:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NG' else 0.) for s,d in panel.items()}
