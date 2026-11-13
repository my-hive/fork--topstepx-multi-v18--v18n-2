"""v18n-2 experiment 323."""
import numpy as np
import pandas as pd
FAMILY="crude_volume_shock_informedflow_continuation"
PARAMS={"volume_mult":8.0,"min_return":0.003,"hold_bars":30,"stop_dollars":0.25}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "CL" not in panel:return ans
 d=panel["CL"];c=d.close.to_numpy();v=d.volume.to_numpy().astype(float);t=d.ct_sec.to_numpy();ss=d.session.to_numpy()
 med=pd.Series(v).shift(1).rolling(60,min_periods=60).median().to_numpy();out=ans["CL"]
 ret=np.r_[0.0,c[1:]/c[:-1]-1.0];i=60;n=len(c)
 while i<n-1:
  if med[i]>0 and v[i]>PARAMS["volume_mult"]*med[i] and abs(ret[i])>=PARAMS["min_return"] and 30600<=t[i]<50000:
   side=1 if ret[i]>0 else -1;a=c[i]
   for j in range(i+1,min(i+1+PARAMS["hold_bars"],n)):
    if ss[j]!=ss[i] or t[j]>=50400 or side*(c[j]-a)<=-PARAMS["stop_dollars"]:break
    out[j]=side
   i+=PARAMS["hold_bars"]
  else:i+=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="CL" else 0.0) for s,d in panel.items()}
