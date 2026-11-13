"""v18n-2 experiment 389."""
import numpy as np
import pandas as pd
FAMILY="canadiandollar_gold_safetyshock_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.004,"trade_start":30600,"trade_end":39600,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6C' not in panel or 'GC' not in panel:return ans
 f,g=panel['6C'],panel['GC'];ix=f.index;cg=g.close.reindex(ix).ffill();r=np.log(cg/cg.shift(PARAMS['lookback'])).to_numpy();c=f.close.to_numpy();t=f.ct_sec.to_numpy();o=ans['6C']
 for p in f.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=-1 if r[i]>0 else 1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='6C' else 0.0) for s,d in panel.items()}
