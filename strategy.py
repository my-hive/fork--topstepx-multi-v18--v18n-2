"""v18n-2 experiment 398."""
import numpy as np
FAMILY="soybean_wheat_usmorning_grainsubstitution_convergence"
PARAMS={"lookback":60,"z_threshold":2.,"trade_start":30600,"trade_end":39600,"stop_dollars":1.}
def signals(panel):
 a={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZS' not in panel or 'ZW' not in panel:return a
 s,w=panel['ZS'],panel['ZW'];cw=w.close.reindex(s.index).ffill();v=np.log(s.close/s.close.shift(60))-np.log(cw/cw.shift(60));z=(v/v.shift().rolling(1200,min_periods=600).std()).to_numpy();x=s.close.to_numpy();t=s.ct_sec.to_numpy();o=a['ZS']
 for p in s.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if 30600<=t[i]<39600 and abs(z[i])>=2:
    side=-1 if z[i]>0 else 1;e=x[i]
    for q in p[k+1:]:
     if t[q]>=39600 or side*(x[q]-e)<=-1:break
     o[q]=side
    break
 return a
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZS' else 0.) for s,d in panel.items()}
