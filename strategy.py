"""v18n-2 experiment 391."""
import numpy as np
import pandas as pd
FAMILY="livecattle_corn_feedcost_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.004,"trade_start":30600,"trade_end":43200,"stop_dollars":0.625}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'LE' not in panel or 'ZC' not in panel:return ans
 l,z=panel['LE'],panel['ZC'];ix=l.index;cz=z.close.reindex(ix).ffill();r=np.log(cz/cz.shift(PARAMS['lookback'])).to_numpy();c=l.close.to_numpy();t=l.ct_sec.to_numpy();o=ans['LE']
 for p in l.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=-1 if r[i]>0 else 1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='LE' else 0.0) for s,d in panel.items()}
