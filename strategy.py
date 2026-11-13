"""v18n-2 experiment 370."""
import numpy as np
import pandas as pd
FAMILY="bitcoin_nasdaq_riskappetite_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.004,"trade_start":30600,"trade_end":39600,"stop_dollars":2500.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'MBT' not in panel or 'NQ' not in panel:return ans
 b,n=panel['MBT'],panel['NQ'];ix=b.index;cn=n.close.reindex(ix).ffill();r=np.log(cn/cn.shift(PARAMS['lookback'])).to_numpy();c=b.close.to_numpy();t=b.ct_sec.to_numpy();o=ans['MBT']
 for p in b.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=1 if r[i]>0 else -1;entry=c[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(c[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='MBT' else 0.0) for s,d in panel.items()}
