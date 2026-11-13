"""v18n-2 experiment 347."""
import numpy as np
import pandas as pd
FAMILY="gold_equity_safehaven_shock_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.003,"trade_start":30600,"trade_end":39600,"stop_dollars":2.5}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "GC" not in panel or "ES" not in panel:return ans
 gc,es=panel["GC"],panel["ES"];ix=gc.index;ce=es.close.reindex(ix).ffill();r=np.log(ce/ce.shift(PARAMS["lookback"])).to_numpy();c=gc.close.to_numpy();t=gc.ct_sec.to_numpy();out=ans["GC"]
 for p in gc.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(r[i])>=PARAMS["threshold"]):continue
   side=-1 if r[i]>0 else 1;entry=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-entry)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="GC" else 0.0) for s,d in panel.items()}
