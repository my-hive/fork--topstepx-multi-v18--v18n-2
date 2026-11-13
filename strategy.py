"""v18n-2 experiment 381."""
import numpy as np
import pandas as pd
FAMILY="crude_longbond_inflationshock_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_dollars":0.25}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel or 'ZB' not in panel:return ans
 c,b=panel['CL'],panel['ZB'];ix=c.index;cb=b.close.reindex(ix).ffill();cc=c.close
 rel=np.log(cc/cc.shift(PARAMS['lookback']))-np.log(cb/cb.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();x=cc.to_numpy();t=c.ct_sec.to_numpy();o=ans['CL']
 for p in c.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=-1 if z[i]>0 else 1;entry=x[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(x[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='CL' else 0.0) for s,d in panel.items()}
