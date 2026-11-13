"""v18n-2 experiment 318."""
import numpy as np
import pandas as pd
FAMILY="sterling_boe_proxy_policyrepricing_continuation"
PARAMS={"reference_end":22500,"trade_start":22560,"trade_end":28800,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6B" not in panel:return ans
 d=panel["6B"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();cal=pd.to_datetime(d.session);day,wd=cal.dt.day.to_numpy(),cal.dt.dayofweek.to_numpy();out=ans["6B"]
 for p in d.groupby("session",sort=False).indices.values():
  if not(wd[p[0]]==3 and day[p[0]]<=7):continue
  a=None;side=0
  for i in p:
   if t[i]==22500:a=c[i];side=1 if c[i]>=c[p[0]] else -1
   elif a is not None and 22560<=t[i]<28800:
    if side*(c[i]-a)<=-0.002:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6B" else 0.0) for s,d in panel.items()}
