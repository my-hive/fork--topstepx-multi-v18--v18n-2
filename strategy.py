"""v18n-2 experiment 48.
FAMILY: copper_high_volume_trend_reversal
Mechanism: high-volume directional copper sessions reflect hedging-flow exhaustion; following
reopen retraces as liquidity normalizes.
Hypothesis: completed HG session volume top quintile and absolute return above median, fade
prior direction next session 17:00 CT to 15:00 CT, $250 stop. Falsification: stress/era/year.
"""
import numpy as np
FAMILY="copper_high_volume_trend_reversal";PARAMS={"volume_quantile":.8,"return_quantile":.6,"lookback_sessions":60,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];o=ans['HG'];c,v,t=d.close.to_numpy(),d.volume.to_numpy(),d.ct_sec.to_numpy();vols=[];rets=[];prior=None;pending=0
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if pending and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if pending*(c[i]-ref)<=-.01:break
    o[i]=pending
  pending=0;end=[i for i in ix if 53400<=t[i]<=54000]
  if not end:continue
  px=c[end[-1]];r=0 if prior is None else px/prior-1;pastv=vols[-60:];pastr=np.abs(rets[-60:])
  if len(pastv)>=60 and v[ix].sum()>=np.quantile(pastv,.8) and abs(r)>=np.quantile(pastr,.6):pending=-int(np.sign(r))
  vols.append(v[ix].sum());rets.append(r);prior=px
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='HG' else 0.) for s,d in panel.items()}
