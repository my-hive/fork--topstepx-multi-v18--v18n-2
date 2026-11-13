"""v18n-2 experiment 385."""
import numpy as np
import pandas as pd
FAMILY="euro_gold_usdsafety_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":25200,"trade_end":39600,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6E' not in panel or 'GC' not in panel:return ans
 e,g=panel['6E'],panel['GC'];ix=e.index;cg=g.close.reindex(ix).ffill();ce=e.close
 rel=np.log(ce/ce.shift(PARAMS['lookback']))-np.log(cg/cg.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=ce.to_numpy();t=e.ct_sec.to_numpy();o=ans['6E']
 for p in e.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=-1 if z[i]>0 else 1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='6E' else 0.0) for s,d in panel.items()}
