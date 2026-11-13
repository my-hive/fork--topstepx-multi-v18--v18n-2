"""v18n-2 experiment 343."""
import numpy as np
import pandas as pd
FAMILY="australiandollar_copperbeta_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.002,"trade_start":61200,"trade_end":75600,"stop_dollars":0.0025}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6A" not in panel or "HG" not in panel:return ans
 au,hg=panel["6A"],panel["HG"];ix=au.index;ch=hg.close.reindex(ix).ffill();r=np.log(ch/ch.shift(PARAMS["lookback"])).to_numpy();c=au.close.to_numpy();t=au.ct_sec.to_numpy();out=ans["6A"]
 for p in au.groupby("session",sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS["trade_start"]<=t[i]<PARAMS["trade_end"] and abs(r[i])>=PARAMS["threshold"]):continue
   side=1 if r[i]>0 else -1;a=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS["trade_end"] or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6A" else 0.0) for s,d in panel.items()}
