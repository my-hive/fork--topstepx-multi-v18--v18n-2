"""v18n-2 experiment 341."""
import numpy as np
import pandas as pd
FAMILY="canadiandollar_crudebeta_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.002,"trade_start":30600,"trade_end":39600,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6C" not in panel or "CL" not in panel:return ans
 ca,cl=panel["6C"],panel["CL"];ix=ca.index;cc=cl.close.reindex(ix).ffill();r=np.log(cc/cc.shift(PARAMS["lookback"])).to_numpy();c=ca.close.to_numpy();t=ca.ct_sec.to_numpy();out=ans["6C"]
 for p in ca.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(r[i])>=PARAMS["threshold"]):continue
   side=1 if r[i]>0 else -1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6C" else 0.0) for s,d in panel.items()}
