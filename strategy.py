"""v18n-2 experiment 348."""
import numpy as np
import pandas as pd
FAMILY="yen_equity_riskoff_shock_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.003,"trade_start":30600,"trade_end":39600,"stop_dollars":0.00002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6J" not in panel or "NQ" not in panel:return ans
 y,nq=panel["6J"],panel["NQ"];ix=y.index;cn=nq.close.reindex(ix).ffill();r=np.log(cn/cn.shift(PARAMS["lookback"])).to_numpy();c=y.close.to_numpy();t=y.ct_sec.to_numpy();out=ans["6J"]
 for p in y.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(r[i])>=PARAMS["threshold"]):continue
   side=-1 if r[i]>0 else 1;entry=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-entry)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6J" else 0.0) for s,d in panel.items()}
