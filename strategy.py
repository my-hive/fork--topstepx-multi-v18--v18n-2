"""v18n-2 experiment 202.
FAMILY: platinum_friday_european_liquidity_reversal
Mechanism: Friday European platinum liquidity impulse fades into the US handover as industrial
hedgers close weekly books.
Hypothesis: fade PL 06:00-07:00 direction 07:00-08:00 Friday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="platinum_friday_european_liquidity_reversal";PARAMS={"weekday":4,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'PL' not in panel:return ans
 d=panel['PL'];out=ans['PL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 21600<=t[i]<25200];bars=[i for i in ix if 25200<=t[i]<28800]
  if dow[ix[0]]!=4 or len(x)<2 or not bars:continue
  side=-np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='PL' else 0.) for s,d in panel.items()}
