"""v18n-2 experiment 162.
FAMILY: canadian_dollar_nasdaq_macro_risk_transfer
Mechanism: an exceptional Canadian-dollar Asia move reflects commodity-risk repricing; US Nasdaq
opens with inverse risk transfer after global macro desks rebalance.
Hypothesis: fade top-quintile 6C 06:00-08:30 move in NQ 08:30-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="canadian_dollar_nasdaq_macro_risk_transfer";PARAMS={"history_sessions":60,"quantile":.8,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'6C','NQ'}<=set(panel):return ans
 x=panel['6C'];a=[]
 for day,g in x.groupby('session',sort=False):
  t=g.ct_sec.to_numpy();ix=np.where((t>=21600)&(t<30600))[0]
  if len(ix)>1:a.append((str(pd.Timestamp(day).date()),g.close.iloc[ix[-1]]-g.close.iloc[ix[0]]))
 hist={};vals=[]
 for day,r in a:
  q=np.quantile(np.abs(vals[-60:]),.8) if len(vals)>=60 else np.inf;hist[day]=-np.sign(r) if abs(r)>=q else 0;vals.append(r)
 d=panel['NQ'];out=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();day=pd.to_datetime(d.session).dt.strftime('%Y-%m-%d').to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  side=hist.get(day[ix[0]],0);bars=[i for i in ix if 30600<=t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-12.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NQ' else 0.) for s,d in panel.items()}
