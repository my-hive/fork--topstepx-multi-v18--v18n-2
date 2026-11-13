"""v18n-2 experiment 326."""
import numpy as np
import pandas as pd
FAMILY="spx_lateday_realizedvolatility_continuation"
PARAMS={"reference_bars":30,"baseline_bars":120,"vol_multiplier":1.5,"trade_end":54000,"stop_points":8.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "ES" not in panel:return ans
 d=panel["ES"];c=d.close.to_numpy();t=d.ct_sec.to_numpy();ss=d.session.to_numpy();out=ans["ES"]
 for p in d.groupby("session",sort=False).indices.values():
  ix=p[(t[p]>=46800)&(t[p]<48600)]
  base=p[(t[p]>=39600)&(t[p]<46800)]
  if len(ix)<30 or len(base)<60:continue
  move=c[ix[-1]]-c[ix[0]];rv=np.ptp(c[ix]);bv=np.ptp(c[base])
  if not move or rv< PARAMS["vol_multiplier"]*bv/4:continue
  side=1 if move>0 else -1;a=c[ix[-1]]
  for i in p:
   if t[i]<48600:continue
   if t[i]>=PARAMS["trade_end"] or side*(c[i]-a)<=-PARAMS["stop_points"]:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="ES" else 0.0) for s,d in panel.items()}
