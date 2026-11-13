"""v18n-2 experiment 337."""
import numpy as np
FAMILY="spx_openingauction_vwap_dislocation_reversion"
PARAMS={"build_start":30600,"build_end":36000,"trade_end":43200,"dislocation_points":12.0,"stop_points":5.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "ES" not in panel:return ans
 d=panel["ES"];c=d.close.to_numpy();v=d.volume.to_numpy();t=d.ct_sec.to_numpy();out=ans["ES"]
 for p in d.groupby("session",sort=False).indices.values():
  x=p[(t[p]>=PARAMS["build_start"])&(t[p]<=PARAMS["build_end"])]
  if len(x)<30:continue
  w=v[x].sum()
  if w<=0:continue
  vw=(c[x]*v[x]).sum()/w;dev=c[x[-1]]-vw
  if abs(dev)<PARAMS["dislocation_points"]:continue
  side=-1 if dev>0 else 1;entered=False;entry=0.0
  for i in p:
   if t[i]<=PARAMS["build_end"]:continue
   if t[i]>=PARAMS["trade_end"]:break
   if not entered:
    if side*(c[i]-vw)<=0:entered=True;entry=c[i]
   elif side*(c[i]-entry)<=-PARAMS["stop_points"]:break
   if entered:out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="ES" else 0.0) for s,d in panel.items()}
