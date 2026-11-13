"""v18n-2 experiment 43.
FAMILY: metals_friday_weekly_trend_continuation
Mechanism: positive completed weekly precious/industrial metal trend retains allocator flow
into Friday before weekend risk transfer; Friday session continues week's direction.
Hypothesis: if prior completed weekly close-over-close is positive, long SI/HG Friday from
17:00 CT reopen through 15:00 CT, $250 stop/leg. Falsification: stress/era/year failure.
"""
import numpy as np
import pandas as pd
FAMILY="metals_friday_weekly_trend_continuation";PARAMS={"stop_dollars":250};PV={'SI':5000.,'HG':25000.}
def _plan(df,pv):
 out=np.zeros(len(df),dtype=np.int64);c,t=df.close.to_numpy(),df.ct_sec.to_numpy();fridays=[]
 for ix in df.groupby('session',sort=False).indices.values():
  day=pd.Timestamp(df.session.iloc[ix[0]]);end=[i for i in ix if 53400<=t[i]<=54000]
  # Only old Friday closes are known at current Friday reopen.
  bullish=len(fridays)>=2 and fridays[-1]>fridays[-2]
  if day.dayofweek==4 and bullish:
   bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
   if len(bars)>1:
    ref=c[bars[0]]
    for i in bars[1:]:
     if c[i]-ref<=-250/pv:break
     out[i]=1
  if day.dayofweek==4 and end:fridays.append(c[end[-1]])
 return out
def signals(panel):return {s:(_plan(d,PV[s]) if s in PV else np.zeros(len(d),dtype=np.int64)) for s,d in panel.items()}
def entry_risk(panel):return {s:np.full(len(d),290. if s in PV else 0.) for s,d in panel.items()}
