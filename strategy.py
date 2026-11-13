"""v18n-2 experiment 387."""
import numpy as np
import pandas as pd
FAMILY="nasdaq_tenyear_duration_shock_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.002,"trade_start":30600,"trade_end":39600,"stop_points":12.5}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel or 'ZN' not in panel:return ans
 n,z=panel['NQ'],panel['ZN'];ix=n.index;cz=z.close.reindex(ix).ffill();r=np.log(cz/cz.shift(PARAMS['lookback'])).to_numpy();c=n.close.to_numpy();t=n.ct_sec.to_numpy();o=ans['NQ']
 for p in n.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=1 if r[i]>0 else -1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_points']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='NQ' else 0.0) for s,d in panel.items()}
