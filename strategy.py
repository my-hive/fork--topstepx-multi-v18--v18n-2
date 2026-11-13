"""v18n-2 experiment 396."""
import numpy as np
FAMILY="spx_gold_safetyshock_delayed_continuation"
PARAMS={"lookback":60,"threshold":.004,"trade_start":30600,"trade_end":39600,"stop_points":5.}
def signals(panel):
 a={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ES' not in panel or 'GC' not in panel:return a
 e,g=panel['ES'],panel['GC'];cg=g.close.reindex(e.index).ffill();r=np.log(cg/cg.shift(60)).to_numpy();c=e.close.to_numpy();t=e.ct_sec.to_numpy();o=a['ES']
 for p in e.groupby('session',sort=False).indices.values():
  for k,i in enumerate(p):
   if 30600<=t[i]<39600 and abs(r[i])>=.004:
    side=-1 if r[i]>0 else 1;v=c[i]
    for q in p[k+1:]:
     if t[q]>=39600 or side*(c[q]-v)<=-5:break
     o[q]=side
    break
 return a
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
