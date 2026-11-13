"""v18n-2 experiment 331."""
import numpy as np
import pandas as pd
FAMILY="corn_soybean_morning_relativestrength_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_dollars":1.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "ZS" not in panel or "ZC" not in panel:return ans
 zs,zc=panel["ZS"],panel["ZC"];ix=zs.index;cc=zc.close.reindex(ix).ffill();cs=zs.close
 rel=np.log(cs/cs.shift(PARAMS["lookback"]))-np.log(cc/cc.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cs.to_numpy();t=zs.ct_sec.to_numpy();out=ans["ZS"]
 for p in zs.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="ZS" else 0.0) for s,d in panel.items()}
