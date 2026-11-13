"""v18n-2 experiment 231.
FAMILY: swissfranc_tuesday_us_to_asia_safehaven_reversal
Mechanism: Tuesday late-US CHF safe-haven hedges reverse in Asian liquidity as macro demand
normalizes before Europe.
Hypothesis: fade completed 14:00-15:00 6S direction 00:00-06:00 Tuesday-session Asia; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="swissfranc_tuesday_us_to_asia_safehaven_reversal";PARAMS={"weekday":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6S' not in panel:return ans
 d=panel['6S'];out=ans['6S'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  late=[i for i in ix if 50400<=t[i]<54000];asia=[i for i in ix if t[i]<21600]
  if dow[ix[0]]!=1 or len(late)<2 or not asia:continue
  side=-np.sign(c[late[-1]]-c[late[0]]);ref=c[asia[0]]
  for i in asia:
   if side*(c[i]-ref)<=-.002:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='6S' else 0.) for s,d in panel.items()}
