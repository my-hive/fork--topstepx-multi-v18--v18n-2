"""v18n-2 experiment 393."""
import numpy as np
FAMILY="soybeanoil_naturalgas_renewablefeedstock_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.,"trade_start":30600,"trade_end":39600,"stop_dollars":.25}
def signals(panel):
 a={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZL' not in panel or 'NG' not in panel:return a
 l,n=panel['ZL'],panel['NG'];cn=n.close.reindex(l.index).ffill();rel=np.log(l.close/l.close.shift(60))-np.log(cn/cn.shift(60));z=(rel/rel.shift().rolling(1200,min_periods=600).std()).to_numpy();c=l.close.to_numpy();t=l.ct_sec.to_numpy();o=a['ZL']
 for p in l.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if 30600<=t[i]<39600 and abs(z[i])>=2:
    side=-1 if z[i]>0 else 1;v=c[i]
    for q in p[k+1:]:
     if t[q]>=39600 or side*(c[q]-v)<=-.25:break
     o[q]=side
    break
 return a
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ZL' else 0.) for s,d in panel.items()}
