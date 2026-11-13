"""v18n-2 experiment 329."""
import numpy as np
import pandas as pd
FAMILY="nasdaq_latesession_volatilitycompression_breakout"
PARAMS={"compression_start":43200,"compression_end":45000,"trade_end":50400,"compression_ratio":0.35,"hold_bars":30,"stop_points":60.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "NQ" not in panel:return ans
 d=panel["NQ"];c=d.close.to_numpy();h=d.high.to_numpy();l=d.low.to_numpy();t=d.ct_sec.to_numpy();out=ans["NQ"]
 for p in d.groupby("session",sort=False).indices.values():
  x=p[(t[p]>=43200)&(t[p]<=45000)];b=p[(t[p]>=34200)&(t[p]<43200)]
  if len(x)<25 or len(b)<60:continue
  r=h[x].max()-l[x].min();br=h[b].max()-l[b].min()
  if r>PARAMS["compression_ratio"]*br:continue
  hi,lo=h[x].max(),l[x].min();side=0;a=0.0
  for i in p:
   if t[i]<=45000:continue
   if t[i]>=PARAMS["trade_end"]:break
   if not side:
    if c[i]>hi:side=1;a=c[i]
    elif c[i]<lo:side=-1;a=c[i]
   elif side*(c[i]-a)<=-PARAMS["stop_points"]:break
   if side:out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="NQ" else 0.0) for s,d in panel.items()}
