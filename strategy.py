"""v18n-2 experiment 218.
FAMILY: gasoline_thirdmonday_refinery_reversal
Mechanism: third-Monday refinery hedge-book balancing unwinds early-week gasoline inventory
pressure through the US session.
Hypothesis: short RB 08:30-15:00 third Mondays; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_thirdmonday_refinery_reversal";PARAMS={"weekday":0,"month_week":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy();nth=((dt.dt.day-1)//7+1).to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 30600<=t[i]<54000]
  if dow[ix[0]]!=0 or nth[ix[0]]!=3 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-.006:break
   out[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
