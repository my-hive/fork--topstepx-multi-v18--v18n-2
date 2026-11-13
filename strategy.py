"""v18n-2 experiment 386."""
import numpy as np
import pandas as pd
FAMILY="russell_nasdaq_intraday_sizerotation_momentum"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":39600,"stop_points":5.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RTY' not in panel or 'NQ' not in panel:return ans
 r,n=panel['RTY'],panel['NQ'];ix=r.index;cn=n.close.reindex(ix).ffill();cr=r.close
 rel=np.log(cr/cr.shift(PARAMS['lookback']))-np.log(cn/cn.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cr.to_numpy();t=r.ct_sec.to_numpy();o=ans['RTY']
 for p in r.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=1 if z[i]>0 else -1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_points']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='RTY' else 0.0) for s,d in panel.items()}
