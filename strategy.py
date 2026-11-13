"""v18n-2 experiment 333."""
import numpy as np
FAMILY="naturalgas_settlement_liquidity_reversal"
PARAMS={"reference_start":46800,"reference_end":48600,"trade_end":50400,"stop_dollars":0.025}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "NG" not in panel:return ans
 d=panel["NG"];c=d.close.to_numpy();t=d.ct_sec.to_numpy();out=ans["NG"]
 for p in d.groupby("session",sort=False).indices.values():
  x=p[(t[p]>=PARAMS["reference_start"])&(t[p]<=PARAMS["reference_end"])]
  if len(x)<20:continue
  move=c[x[-1]]-c[x[0]]
  if not move:continue
  side=-1 if move>0 else 1;a=c[x[-1]]
  for i in p:
   if t[i]<=PARAMS["reference_end"]:continue
   if t[i]>=PARAMS["trade_end"] or side*(c[i]-a)<=-PARAMS["stop_dollars"]:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="NG" else 0.0) for s,d in panel.items()}
