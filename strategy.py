"""v18n-2 experiment 400."""
import numpy as np
FAMILY="leanhog_corn_feedcost_delayed_continuation"
PARAMS={"lookback":60,"threshold":.004,"trade_start":30600,"trade_end":43200,"stop_dollars":.625}
def signals(panel):
 a={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HE' not in panel or 'ZC' not in panel:return a
 h,z=panel['HE'],panel['ZC'];cz=z.close.reindex(h.index).ffill();r=np.log(cz/cz.shift(60)).to_numpy();c=h.close.to_numpy();t=h.ct_sec.to_numpy();o=a['HE']
 for p in h.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if 30600<=t[i]<43200 and abs(r[i])>=.004:
    side=-1 if r[i]>0 else 1;e=c[i]
    for q in p[k+1:]:
     if t[q]>=43200 or side*(c[q]-e)<=-.625:break
     o[q]=side
    break
 return a
def entry_risk(panel):return {s:np.full(len(d),250. if s=='HE' else 0.) for s,d in panel.items()}
