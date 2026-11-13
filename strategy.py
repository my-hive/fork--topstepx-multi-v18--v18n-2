"""v18n-2 experiment 351."""
import numpy as np
import pandas as pd
FAMILY="soybean_soybeanoil_morning_crushspread_convergence"
PARAMS={"lookback":60,"z_threshold":2.0,"trade_start":30600,"trade_end":41400,"stop_dollars":0.25}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZL' not in panel or 'ZS' not in panel:return ans
 l,s=panel['ZL'],panel['ZS'];ix=l.index;cs=s.close.reindex(ix).ffill();cl=l.close
 rel=np.log(cl/cl.shift(PARAMS['lookback']))-np.log(cs/cs.shift(PARAMS['lookback']))
 z=(rel/rel.shift(1).rolling(1200,min_periods=600).std()).to_numpy();c=cl.to_numpy();t=l.ct_sec.to_numpy();o=ans['ZL']
 for p in l.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if not(PARAMS['trade_start']<=t[i]<PARAMS['trade_end'] and abs(z[i])>=PARAMS['z_threshold']):continue
   side=-1 if z[i]>0 else 1;entry=c[i]
   for j in p[k+1:]:
    if t[j]>=PARAMS['trade_end'] or side*(c[j]-entry)<=-PARAMS['stop_dollars']:break
    o[j]=side
   break
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=='ZL' else 0.0) for s,d in panel.items()}
