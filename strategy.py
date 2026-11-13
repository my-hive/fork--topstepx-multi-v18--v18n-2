"""v18n-2 experiment 360."""
import numpy as np
import pandas as pd
FAMILY="sterling_treasury_rateshock_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.002,"trade_start":25200,"trade_end":39600,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6B' not in panel or 'ZN' not in panel:return ans
 b,z=panel['6B'],panel['ZN'];ix=b.index;cz=z.close.reindex(ix).ffill();r=np.log(cz/cz.shift(PARAMS['lookback'])).to_numpy();c=b.close.to_numpy();t=b.ct_sec.to_numpy();o=ans['6B']
 for p in b.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=-1 if r[i]>0 else 1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='6B' else 0.0) for s,d in panel.items()}
