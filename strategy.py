"""v18n-2 experiment 334."""
import numpy as np
import pandas as pd
FAMILY="fiveyear_tenyear_curve_relativestrength_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":28800,"trade_end":39600,"stop_ticks":0.125}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "ZF" not in panel or "ZN" not in panel:return ans
 zf,zn=panel["ZF"],panel["ZN"];ix=zf.index;cn=zn.close.reindex(ix).ffill();cf=zf.close
 rel=np.log(cf/cf.shift(PARAMS["lookback"]))-np.log(cn/cn.shift(PARAMS["lookback"]))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cf.to_numpy();t=zf.ct_sec.to_numpy();out=ans["ZF"]
 for p in zf.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(z[i])>=PARAMS["z_threshold"]):continue
   side=-1 if z[i]>0 else 1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_ticks"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="ZF" else 0.0) for s,d in panel.items()}
