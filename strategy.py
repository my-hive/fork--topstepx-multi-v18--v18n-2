"""v18n-2 experiment 332."""
import numpy as np
import pandas as pd
FAMILY="euro_sterling_morning_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":25200,"trade_end":34200,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6E" not in panel or "6B" not in panel:return ans
 eu,gb=panel["6E"],panel["6B"];ix=eu.index;cg=gb.close.reindex(ix).ffill();ce=eu.close
 rel=np.log(ce/ce.shift(PARAMS["lookback"]))-np.log(cg/cg.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=ce.to_numpy();t=eu.ct_sec.to_numpy();out=ans["6E"]
 for p in eu.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6E" else 0.0) for s,d in panel.items()}
