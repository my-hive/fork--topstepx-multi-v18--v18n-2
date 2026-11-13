"""v18n-2 experiment 335."""
import numpy as np
import pandas as pd
FAMILY="livecattle_leanhog_morning_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_dollars":0.625}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "HE" not in panel or "LE" not in panel:return ans
 he,le=panel["HE"],panel["LE"];ix=he.index;cl=le.close.reindex(ix).ffill();ch=he.close
 rel=np.log(ch/ch.shift(PARAMS["lookback"]))-np.log(cl/cl.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=ch.to_numpy();t=he.ct_sec.to_numpy();out=ans["HE"]
 for p in he.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="HE" else 0.0) for s,d in panel.items()}
