"""v18n-2 experiment 366."""
import numpy as np
import pandas as pd
FAMILY="mexicanpeso_crude_delayed_commoditycurrency_continuation"
PARAMS={"lookback":60,"threshold":0.005,"trade_start":30600,"trade_end":39600,"stop_dollars":0.00005}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6M' not in panel or 'CL' not in panel:return ans
 m,c=panel['6M'],panel['CL'];ix=m.index;cc=c.close.reindex(ix).ffill();r=np.log(cc/cc.shift(PARAMS['lookback'])).to_numpy();x=m.close.to_numpy();t=m.ct_sec.to_numpy();o=ans['6M']
 for p in m.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=1 if r[i]>0 else -1;entry=x[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(x[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='6M' else 0.0) for s,d in panel.items()}
