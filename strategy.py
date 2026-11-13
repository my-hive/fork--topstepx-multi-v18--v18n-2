"""v18n-2 experiment 377."""
import numpy as np
import pandas as pd
FAMILY="longbond_tenyear_curve_steepening_momentum"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":25200,"trade_end":39600,"stop_dollars":0.5}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel or 'ZN' not in panel:return ans
 b,n=panel['ZB'],panel['ZN'];ix=b.index;cn=n.close.reindex(ix).ffill();cb=b.close
 rel=np.log(cb/cb.shift(PARAMS['lookback']))-np.log(cn/cn.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cb.to_numpy();t=b.ct_sec.to_numpy();o=ans['ZB']
 for p in b.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=1 if z[i]>0 else -1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='ZB' else 0.0) for s,d in panel.items()}
