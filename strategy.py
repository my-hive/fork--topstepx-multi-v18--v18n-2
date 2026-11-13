"""v18n-2 experiment 324."""
import numpy as np
import pandas as pd
FAMILY="gold_volatilitycompression_expansion_breakout"
PARAMS={"range_bars":60,"baseline_bars":1800,"compression_quantile":0.1,"hold_bars":30,"stop_dollars":2.5}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "GC" not in panel:return ans
 d=panel["GC"];c=d.close.to_numpy();h=d.high.to_numpy();l=d.low.to_numpy();t=d.ct_sec.to_numpy();ss=d.session.to_numpy();n=len(d);out=ans["GC"]
 r=pd.Series(h).rolling(PARAMS["range_bars"],min_periods=PARAMS["range_bars"]).max()-pd.Series(l).rolling(PARAMS["range_bars"],min_periods=PARAMS["range_bars"]).min()
 q=r.shift(1).rolling(PARAMS["baseline_bars"],min_periods=PARAMS["baseline_bars"]).quantile(PARAMS["compression_quantile"]).to_numpy();rv=r.to_numpy();i=PARAMS["range_bars"]+PARAMS["baseline_bars"]
 while i<n-1:
  if rv[i]<=q[i] and 3600<=t[i]<46800:
   hi=h[i-PARAMS["range_bars"]+1:i+1].max();lo=l[i-PARAMS["range_bars"]+1:i+1].min();side=0
   for k in range(i+1,min(i+31,n)):
    if ss[k]!=ss[i] or t[k]>=50400:break
    if c[k]>hi:side=1;break
    if c[k]<lo:side=-1;break
   if side:
    a=c[k]
    for j in range(k+1,min(k+1+PARAMS["hold_bars"],n)):
     if ss[j]!=ss[k] or t[j]>=50400 or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
     out[j]=side
    i=k+PARAMS["hold_bars"]
   else:i+=1
  else:i+=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="GC" else 0.0) for s,d in panel.items()}
