"""v18n-2 experiment 336."""
import numpy as np
import pandas as pd
FAMILY="heatingoil_crude_morning_crackspread_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_dollars":0.025}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "HO" not in panel or "CL" not in panel:return ans
 ho,cl=panel["HO"],panel["CL"];ix=ho.index;cc=cl.close.reindex(ix).ffill();ch=ho.close
 rel=np.log(ch/ch.shift(PARAMS["lookback"]))-np.log(cc/cc.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=ch.to_numpy();t=ho.ct_sec.to_numpy();out=ans["HO"]
 for p in ho.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="HO" else 0.0) for s,d in panel.items()}
