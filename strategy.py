"""v18n-2 experiment 242.
FAMILY: heatingoil_december_refinery_hedge_reversal
Mechanism: December heating-oil winter supply hedging creates opening excess reversed during US
physical liquidity.
Hypothesis: short HO 08:30-15:00 in December; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="heatingoil_december_refinery_hedge_reversal";PARAMS={"month":12,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HO' not in panel:return ans
 d=panel['HO'];out=ans['HO'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mon[ix[0]]!=12 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-.006:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HO' else 0.) for s,d in panel.items()}
