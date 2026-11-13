"""v18n-2 experiment 185.
FAMILY: heatingoil_tuesday_midday_refinery_hedge_reversal
Mechanism: Tuesday late-morning heating-oil refinery hedge flow overextends then reverses as
physical inventory liquidity clears through the afternoon.
Hypothesis: fade HO 11:00-12:00 direction 12:00-15:00 Tuesday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="heatingoil_tuesday_midday_refinery_hedge_reversal";PARAMS={"weekday":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HO' not in panel:return ans
 d=panel['HO'];out=ans['HO'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 39600<=t[i]<43200];bars=[i for i in ix if 43200<=t[i]<54000]
  if dow[ix[0]]!=1 or len(x)<2 or not bars:continue
  side=-np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.006:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HO' else 0.) for s,d in panel.items()}
