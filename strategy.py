"""v18n-2 experiment 167.
FAMILY: nasdaq_firstweek_monday_institutional_rebalance
Mechanism: first-week Monday pension and systematic allocation demand persists into US afternoon
index liquidity.
Hypothesis: long NQ first-calendar-week Mondays 12:00-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="nasdaq_firstweek_monday_institutional_rebalance";PARAMS={"calendar_week":1,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];out=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dt=pd.to_datetime(d.session);dow=dt.dt.dayofweek.to_numpy();wk=((dt.dt.day-1)//7+1).to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 43200<=t[i]<54000]
  if dow[ix[0]]!=0 or wk[ix[0]]!=1 or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-12.5:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NQ' else 0.) for s,d in panel.items()}
