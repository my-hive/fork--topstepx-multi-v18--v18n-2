"""v18n-2 experiment 90.
FAMILY: crude_tuesday_trend_reversal
Mechanism: after a three-session CL gain, Tuesday inventory hedging absorbs residual long
speculative flow during US hours.
Hypothesis: short CL Tuesday 08:30-15:00 after positive trailing 3-session return, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="crude_tuesday_trend_reversal";PARAMS={"lookback_days":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];o=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();days=list(d.groupby('session',sort=False).indices.values());rs=[]
 for n,ix in enumerate(days):
  side=pd.Timestamp(d.session.iloc[ix[0]]).dayofweek==1 and n>=3 and sum(rs[-3:])>0
  bars=[i for i in ix if 30600<=t[i]<54000]
  if side and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if ref-c[i]<=-.25:break
    o[i]=-1
  rs.append(c[ix[-1]]/c[ix[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='CL' else 0.) for s,d in panel.items()}
