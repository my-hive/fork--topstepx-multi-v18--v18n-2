"""v18n-2 experiment 327."""
import numpy as np
import pandas as pd
FAMILY="nq_es_relativestrength_convergence_spread"
PARAMS={"lookback":60,"z_threshold":2.0,"hold_bars":30,"stop_points":60.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "ES" not in panel or "NQ" not in panel:return ans
 es,nq=panel["ES"],panel["NQ"];ix=nq.index
 ce=es.close.reindex(ix).ffill();cn=nq.close
 sp=np.log(cn/cn.shift(PARAMS["lookback"]))-np.log(ce/ce.shift(PARAMS["lookback"]))
 z=(sp/sp.shift(1).rolling(1200,min_periods=600).std()).to_numpy();t=nq.ct_sec.to_numpy();ss=nq.session.to_numpy();c=cn.to_numpy();n=len(nq);out=ans["NQ"];i=1200
 while i<n-1:
  if abs(z[i])>=PARAMS["z_threshold"] and 31200<=t[i]<50000:
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in range(i+1,min(i+1+PARAMS["hold_bars"],n)):
    if ss[j]!=ss[i] or t[j]>=50400 or side*(c[j]-a)<=-PARAMS["stop_points"]:break
    out[j]=side
   i+=PARAMS["hold_bars"]
  else:i+=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="NQ" else 0.0) for s,d in panel.items()}
