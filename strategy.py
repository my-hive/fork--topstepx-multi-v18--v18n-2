"""v18n-2 experiment 328."""
import numpy as np
import pandas as pd
FAMILY="nq_es_relativestrength_twoleg_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"hold_bars":30,"stop_dollars":250.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "ES" not in panel or "NQ" not in panel:return ans
 es,nq=panel["ES"],panel["NQ"];ix=nq.index
 ce=es.close.reindex(ix).ffill();cn=nq.close
 sp=np.log(cn/cn.shift(PARAMS["lookback"]))-np.log(ce/ce.shift(PARAMS["lookback"]))
 z=(sp/sp.shift(1).rolling(1200,min_periods=600).std()).to_numpy();t=nq.ct_sec.to_numpy();ss=nq.session.to_numpy();cnn=cn.to_numpy();cee=ce.to_numpy();n=len(nq);on=ans["NQ"];oe=ans["ES"]
 ep=es.index;pos=ep.get_indexer(ix,method="ffill")
 i=1200
 while i<n-1:
  if abs(z[i])>=PARAMS["z_threshold"] and 31200<=t[i]<50000 and pos[i]>=0:
   side=-1 if z[i]>0 else 1;an,ae=cnn[i],cee[i]
   for j in range(i+1,min(i+1+PARAMS["hold_bars"],n)):
    pnl=side*(cnn[j]-an)*20-side*(cee[j]-ae)*50
    if ss[j]!=ss[i] or t[j]>=50400 or pnl<=-PARAMS["stop_dollars"]:break
    on[j]=side
    if pos[j]>=0 and es.index[pos[j]]==ix[j]:oe[pos[j]]=-side
   i+=PARAMS["hold_bars"]
  else:i+=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),150.0 if s in("ES","NQ") else 0.0) for s,d in panel.items()}
