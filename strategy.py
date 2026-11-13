"""v18n-2 experiment 346."""
import numpy as np
import pandas as pd
FAMILY="aud_nzd_asia_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":64800,"trade_end":75600,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6N" not in panel or "6A" not in panel:return ans
 n,a=panel["6N"],panel["6A"];ix=n.index;ca=a.close.reindex(ix).ffill();cn=n.close
 rel=np.log(cn/cn.shift(PARAMS["lookback"]))-np.log(ca/ca.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cn.to_numpy();t=n.ct_sec.to_numpy();out=ans["6N"]
 for p in n.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;entry=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-entry)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6N" else 0.0) for s,d in panel.items()}
