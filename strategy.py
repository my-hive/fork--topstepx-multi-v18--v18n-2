"""v18n-2 experiment 46.
FAMILY: precious_metals_joint_overnight_shock_continuation
Mechanism: concurrent extreme same-direction gold and silver overnight moves identify a
common monetary-information shock rather than metal-specific noise; COMEX session continues.
Hypothesis: both completed overnight returns are top-decile vs trailing 60 sessions and agree;
trade both same direction 08:30-15:00 CT, $250 stop each. Falsification: stress/era/year fail.
"""
import numpy as np
FAMILY="precious_metals_joint_overnight_shock_continuation";PARAMS={"quantile":.9,"lookback_sessions":60,"stop_dollars":250};PV={'GC':100.,'SI':5000.}
def _moves(df):
 c,t=df.close.to_numpy(),df.ct_sec.to_numpy();out=[]
 for ix in df.groupby('session',sort=False).indices.values():
  x=[i for i in ix if t[i]>=61200 or t[i]<30600];out.append(c[x[-1]]/c[x[0]]-1 if len(x)>1 else np.nan)
 return out
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not set(PV)<=set(panel):return ans
 a,b=_moves(panel['GC']),_moves(panel['SI']); sides=[]
 for n,(x,y) in enumerate(zip(a,b)):
  pa,pb=np.abs(a[max(0,n-60):n]),np.abs(b[max(0,n-60):n]);sides.append(int(np.sign(x)) if len(pa)>=60 and np.sign(x)==np.sign(y) and abs(x)>=np.quantile(pa,.9) and abs(y)>=np.quantile(pb,.9) else 0)
 for s in PV:
  d=panel[s];o=ans[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
  for n,ix in enumerate(d.groupby('session',sort=False).indices.values()):
   side=sides[n] if n<len(sides) else 0;e=[i for i in ix if 30600<=t[i]<54000]
   if not side or not e:continue
   ref=c[e[0]]
   for i in e:
    if side*(c[i]-ref)<=-250/PV[s]:break
    o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s in PV else 0.) for s,d in panel.items()}
