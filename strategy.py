"""v18n-2 experiment 372."""
import numpy as np
import pandas as pd
FAMILY="microcrude_nasdaq_macrogrowth_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.004,"trade_start":30600,"trade_end":39600,"stop_dollars":0.25}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'MCL' not in panel or 'NQ' not in panel:return ans
 c,n=panel['MCL'],panel['NQ'];ix=c.index;cn=n.close.reindex(ix).ffill();r=np.log(cn/cn.shift(PARAMS['lookback'])).to_numpy();x=c.close.to_numpy();t=c.ct_sec.to_numpy();o=ans['MCL']
 for p in c.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=1 if r[i]>0 else -1;entry=x[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(x[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='MCL' else 0.0) for s,d in panel.items()}
