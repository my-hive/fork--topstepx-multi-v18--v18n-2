"""v18n-2 experiment 364."""
import numpy as np
import pandas as pd
FAMILY="platinum_gold_industrialprecious_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_dollars":25.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'PL' not in panel or 'GC' not in panel:return ans
 p,g=panel['PL'],panel['GC'];ix=p.index;cg=g.close.reindex(ix).ffill();cp=p.close
 rel=np.log(cp/cp.shift(PARAMS['lookback']))-np.log(cg/cg.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cp.to_numpy();t=p.ct_sec.to_numpy();o=ans['PL']
 for q in p.groupby('session',sort=False).indices.values():
  for k,i in enumerate(q):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=-1 if z[i]>0 else 1;entry=c[i]
   for r in q[k+1:]:
    if t[r]>=PARAMS['trade_end'] or side*(c[r]-entry)<=-PARAMS['stop_dollars']:break
    o[r]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='PL' else 0.0) for s,d in panel.items()}
