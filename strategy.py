"""v18n-2 experiment 344."""
import numpy as np
import pandas as pd
FAMILY="gold_silver_intraday_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_dollars":0.25}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "SI" not in panel or "GC" not in panel:return ans
 si,gc=panel["SI"],panel["GC"];ix=si.index;cg=gc.close.reindex(ix).ffill();cs=si.close
 rel=np.log(cs/cs.shift(PARAMS["lookback"]))-np.log(cg/cg.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cs.to_numpy();t=si.ct_sec.to_numpy();out=ans["SI"]
 for p in si.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="SI" else 0.0) for s,d in panel.items()}
