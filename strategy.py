"""v18n-2 experiment 45.
FAMILY: gold_asia_range_us_breakout_continuation
Mechanism: Asian gold range contains overnight information; US COMEX break releases
participation and continues through afternoon.
Hypothesis: completed 17:00-08:30 CT GC range break after 08:30, follow first breakout to
15:00 CT, $250 stop, one trade/session. Falsification: stressed/era/year failure.
"""
import numpy as np
FAMILY="gold_asia_range_us_breakout_continuation";PARAMS={"range_end":30600,"exit_sec":54000,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  a=[i for i in ix if t[i]>=61200 or t[i]<30600];u=[i for i in ix if 30600<=t[i]<54000]
  if not a or not u:continue
  hi,lo=h[a].max(),l[a].min();side=0;ref=0.
  for i in u:
   if not side:
    if c[i]>hi:side,ref=1,c[i]
    elif c[i]<lo:side,ref=-1,c[i]
   if side:
    if side*(c[i]-ref)<=-2.5:break
    o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
