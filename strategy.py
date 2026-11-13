"""v18n-2 experiment 399."""
import numpy as np
FAMILY="rbob_naturalgas_energydemand_relativevalue_convergence"
PARAMS={"lookback":60,"z_threshold":2.,"trade_start":30600,"trade_end":39600,"stop_dollars":.006}
def signals(panel):
 a={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel or 'NG' not in panel:return a
 r,n=panel['RB'],panel['NG'];cn=n.close.reindex(r.index).ffill();v=np.log(r.close/r.close.shift(60))-np.log(cn/cn.shift(60));z=(v/v.shift().rolling(1200,min_periods=600).std()).to_numpy();x=r.close.to_numpy();t=r.ct_sec.to_numpy();o=a['RB']
 for p in r.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if 30600<=t[i]<39600 and abs(z[i])>=2:
    side=-1 if z[i]>0 else 1;e=x[i]
    for q in p[k+1:]:
     if t[q]>=39600 or side*(x[q]-e)<=-.006:break
     o[q]=side
    break
 return a
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
