"""v18n-2 experiment 181.
FAMILY: feeder_cattle_monday_lunch_processor_hedge_reversal
Mechanism: Monday late-morning feeder-cattle processor hedge flow overextends and reverses through
lunch as physical order flow clears.
Hypothesis: short LE 11:00-12:00 direction (fade) 12:00-13:00 Monday; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="feeder_cattle_monday_lunch_processor_hedge_reversal";PARAMS={"weekday":0,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'LE' not in panel:return ans
 d=panel['LE'];out=ans['LE'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dow=pd.to_datetime(d.session).dt.dayofweek.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 39600<=t[i]<43200];bars=[i for i in ix if 43200<=t[i]<46800]
  if dow[ix[0]]!=0 or len(x)<2 or not bars:continue
  side=-np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='LE' else 0.) for s,d in panel.items()}
