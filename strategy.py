"""v18n-2 experiment 317."""
import numpy as np
import pandas as pd
FAMILY="canadiandollar_boc_proxy_policyrepricing_continuation"
PARAMS={"reference_end":33300,"trade_start":33360,"trade_end":39600,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "6C" not in panel:return ans
 d=panel["6C"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();cal=pd.to_datetime(d.session);day,wd=cal.dt.day.to_numpy(),cal.dt.dayofweek.to_numpy();out=ans["6C"]
 for p in d.groupby("session",sort=False).indices.values():
  if not(wd[p[0]]==2 and day[p[0]]<=7):continue
  a=None;side=0
  for i in p:
   if t[i]==33300:a=c[i];side=1 if c[i]>=c[p[0]] else -1
   elif a is not None and 33360<=t[i]<39600:
    if side*(c[i]-a)<=-0.002:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="6C" else 0.0) for s,d in panel.items()}
