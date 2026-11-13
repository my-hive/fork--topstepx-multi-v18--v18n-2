"""v18n-2 experiment 263.
FAMILY: soybeans_september_harvest_supply_reversal
Mechanism: September harvest hedge supply creates soybean selling through US cash liquidity.
Hypothesis: short ZS 08:30-15:00 in September; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="soybeans_september_harvest_supply_reversal";PARAMS={"month":9,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZS' not in panel:return ans
 d=panel['ZS'];out=ans['ZS'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mon=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if mon[ix[0]]!=9 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-5.:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZS' else 0.) for s,d in panel.items()}
