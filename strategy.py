"""v18n-2 experiment 368."""
import numpy as np
import pandas as pd
FAMILY="soybeanoil_heatingoil_renewablefuel_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_dollars":0.006}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HO' not in panel or 'ZL' not in panel:return ans
 h,l=panel['HO'],panel['ZL'];ix=h.index;cl=l.close.reindex(ix).ffill();ch=h.close
 rel=np.log(ch/ch.shift(PARAMS['lookback']))-np.log(cl/cl.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=ch.to_numpy();t=h.ct_sec.to_numpy();o=ans['HO']
 for p in h.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=-1 if z[i]>0 else 1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='HO' else 0.0) for s,d in panel.items()}
