"""v18n-2 experiment 378."""
import numpy as np
import pandas as pd
FAMILY="ultrabond_longbond_durationtails_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":25200,"trade_end":39600,"stop_dollars":0.5}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'UB' not in panel or 'ZB' not in panel:return ans
 u,b=panel['UB'],panel['ZB'];ix=u.index;cb=b.close.reindex(ix).ffill();cu=u.close
 rel=np.log(cu/cu.shift(PARAMS['lookback']))-np.log(cb/cb.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cu.to_numpy();t=u.ct_sec.to_numpy();o=ans['UB']
 for p in u.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=-1 if z[i]>0 else 1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='UB' else 0.0) for s,d in panel.items()}
