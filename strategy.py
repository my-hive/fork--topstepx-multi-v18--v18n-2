"""v18n-2 experiment 350."""
import numpy as np
import pandas as pd
FAMILY="corn_naturalgas_fertilizercost_delayed_continuation"
PARAMS={"lookback":60,"threshold":0.006,"trade_start":30600,"trade_end":41400,"stop_points":0.125}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZC' not in panel or 'NG' not in panel:return ans
 z,n=panel['ZC'],panel['NG'];ix=z.index;cn=n.close.reindex(ix).ffill();r=np.log(cn/cn.shift(PARAMS['lookback'])).to_numpy();c=z.close.to_numpy();t=z.ct_sec.to_numpy();o=ans['ZC']
 for p in z.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(r[i])>=PARAMS['threshold']):continue
   side=1 if r[i]>0 else -1;entry=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS['trade_end'] or side*(c[j]-entry)<=-PARAMS['stop_points']:break
    o[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='ZC' else 0.0) for s,d in panel.items()}
