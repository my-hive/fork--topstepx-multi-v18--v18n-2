"""v18n-2 experiment 340."""
import numpy as np
FAMILY="spx_overnight_cashopen_acceptance_continuation"
PARAMS={"overnight_start":61200,"open":30600,"confirm_end":31500,"trade_end":39600,"stop_points":5.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "ES" not in panel:return ans
 d=panel["ES"];c=d.close.to_numpy();t=d.ct_sec.to_numpy();out=ans["ES"]
 for p in d.groupby("session",sort=False).indices.values():
  pre=p[(t[p]>=PARAMS["overnight_start"])|(t[p]<PARAMS["open"])]
  first=p[(t[p]>=PARAMS["open"])&(t[p]<=PARAMS["confirm_end"])]
  if len(pre)<30 or len(first)<10:continue
  side=1 if c[pre[-1]]>c[pre[0]] else -1
  opening=c[first[-1]]-c[first[0]]
  if side*opening<=0:continue
  a=c[first[-1]]
  for i in p:
   if t[i]<=PARAMS["confirm_end"]:continue
   if t[i]>=PARAMS["trade_end"] or side*(c[i]-a)<=-PARAMS["stop_points"]:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="ES" else 0.0) for s,d in panel.items()}
