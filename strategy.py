"""v18n-2 experiment 330."""
import numpy as np
import pandas as pd
FAMILY="rbob_crude_morning_relativestrength_reversal"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":32400,"trade_end":39600,"stop_dollars":0.25}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "RB" not in panel or "CL" not in panel:return ans
 rb,cl=panel["RB"],panel["CL"];ix=rb.index;cc=cl.close.reindex(ix).ffill();cr=rb.close
 rel=np.log(cr/cr.shift(PARAMS["lookback"]))-np.log(cc/cc.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cr.to_numpy();t=rb.ct_sec.to_numpy();ss=rb.session.to_numpy();out=ans["RB"]
 for p in rb.groupby("session",sort=False).indices.values():
  for i in p:
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[np.searchsorted(p,i)+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="RB" else 0.0) for s,d in panel.items()}
