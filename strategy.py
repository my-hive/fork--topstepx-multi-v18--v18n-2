"""v18n-2 experiment 339."""
import numpy as np
import pandas as pd
FAMILY="spx_dow_morning_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_points":50.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "YM" not in panel or "ES" not in panel:return ans
 ym,es=panel["YM"],panel["ES"];ix=ym.index;ce=es.close.reindex(ix).ffill();cy=ym.close
 rel=np.log(cy/cy.shift(PARAMS["lookback"]))-np.log(ce/ce.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cy.to_numpy();t=ym.ct_sec.to_numpy();out=ans["YM"]
 for p in ym.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_points"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="YM" else 0.0) for s,d in panel.items()}
