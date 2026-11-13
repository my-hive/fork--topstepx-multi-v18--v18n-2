"""v18n-2 experiment 72.
FAMILY: dow_monday_positive_feedback
Mechanism: Friday broad-industrial risk-on positioning persists into Monday as systematic
allocators and pension rebalancers add liquid blue-chip beta.
Hypothesis: after positive Friday, long YM Monday 17:00 CT through 15:00 CT, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="dow_monday_positive_feedback";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'YM' not in panel:return ans
 d=panel['YM'];o=ans['YM'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();days=list(d.groupby('session',sort=False).indices.values());rets=[]
 for n,ix in enumerate(days):
  side=pd.Timestamp(d.session.iloc[ix[0]]).dayofweek==0 and n and rets[-1]>0
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if side and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if c[i]-ref<=-50.:break
    o[i]=1
  rets.append(c[ix[-1]]/c[ix[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='YM' else 0.) for s,d in panel.items()}
