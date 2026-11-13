"""v18n-2 experiment 175.
FAMILY: euro_wednesday_london_liquidity_reversal
Mechanism: Wednesday European corporate/real-money FX hedging creates a pre-London-fix 04:00-05:00
EUR future overshoot, reversed as London liquidity broadens in following hour.
Hypothesis: short 6E 05:00-06:00 Wednesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="euro_wednesday_london_liquidity_reversal";PARAMS={"weekday":2,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6E' not in panel:return ans
 d=panel['6E'];out=ans['6E'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 18000<=t[i]<21600]
  if dow[ix[0]]!=2 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref>=.002:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='6E' else 0.) for s,d in panel.items()}
