"""v18n-2 experiment 367."""
import numpy as np
import pandas as pd
FAMILY="canadiandollar_naturalgas_delayed_energycurrency_continuation"
PARAMS={"lookback":60,"threshold":0.006,"trade_start":30600,"trade_end":39600,"stop_dollars":0.002}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if '6C' not in panel or 'NG' not in panel:return ans
 c,n=panel['6C'],panel['NG'];ix=c.index;cn=n.close.reindex(ix).ffill();r=np.log(cn/cn.shift(PARAMS['lookback'])).to_numpy();x=c.close.to_numpy();t=c.ct_sec.to_numpy();o=ans['6C']
 for p in c.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=1 if r[i]>0 else -1;entry=x[i]
   for q in p[k+1:]:
    if t[q]>=PARAMS['trade_end'] or side*(x[q]-entry)<=-PARAMS['stop_dollars']:break
    o[q]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='6C' else 0.0) for s,d in panel.items()}
