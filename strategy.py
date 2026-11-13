"""v18n-2 experiment 384."""
import numpy as np
import pandas as pd
FAMILY="corn_crude_ethanolmargin_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.006,"trade_start":30600,"trade_end":41400,"stop_points":0.125}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZC' not in panel or 'CL' not in panel:return ans
 z,c=panel['ZC'],panel['CL'];ix=z.index;cc=c.close.reindex(ix).ffill();r=np.log(cc/cc.shift(PARAMS['lookback'])).to_numpy();x=z.close.to_numpy();t=z.ct_sec.to_numpy();o=ans['ZC']
 for p in z.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=1 if r[i]>0 else -1;entry=x[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(x[q]-entry)<=-PARAMS['stop_points']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='ZC' else 0.0) for s,d in panel.items()}
