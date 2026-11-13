"""v18n-2 experiment 320."""
import numpy as np
import pandas as pd
FAMILY="euro_ecb_proxy_policyrepricing_continuation"
PARAMS={"reference_end":27000,"trade_start":27060,"trade_end":32400,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6E" not in panel:return ans
 d=panel["6E"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();cal=pd.to_datetime(d.session);day,wd=cal.dt.day.to_numpy(),cal.dt.dayofweek.to_numpy();out=ans["6E"]
 for p in d.groupby("session",sort=False).indices.values():
  if not(wd[p[0]]==3 and 8<=day[p[0]]<=14):continue
  a=None;side=0
  for i in p:
   if t[i]==27000:a=c[i];side=1 if c[i]>=c[p[0]] else -1
   elif a is not None and 27060<=t[i]<32400:
    if side*(c[i]-a)<=-0.002:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6E" else 0.0) for s,d in panel.items()}
