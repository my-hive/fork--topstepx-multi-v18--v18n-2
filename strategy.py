"""v18n-2 experiment 325."""
import numpy as np
import pandas as pd
FAMILY="euro_overnight_liquidityvacuum_openingrange_continuation"
PARAMS={"range_start":21600,"range_end":25200,"trade_end":30600,"volume_ratio":0.7,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6E" not in panel:return ans
 d=panel["6E"];c=d.close.to_numpy();h=d.high.to_numpy();l=d.low.to_numpy();v=d.volume.to_numpy().astype(float);t=d.ct_sec.to_numpy();ss=d.session.to_numpy();out=ans["6E"]
 med=pd.Series(v).shift(1).rolling(60,min_periods=60).median().to_numpy()
 for p in d.groupby("session",sort=False).indices.values():
  ix=p[(t[p]>=21600)&(t[p]<=25200)]
  if len(ix)<30 or med[ix[-1]]<=0 or v[ix].mean()>PARAMS["volume_ratio"]*med[ix[-1]]:continue
  hi=h[ix].max();lo=l[ix].min();side=0;a=0.0
  for i in p:
   if t[i]<=25200:continue
   if t[i]>=30600:break
   if not side:
    if c[i]>hi:side=1;a=c[i]
    elif c[i]<lo:side=-1;a=c[i]
   elif side*(c[i]-a)<=-PARAMS["stop_dollars"]:break
   if side:out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6E" else 0.0) for s,d in panel.items()}
