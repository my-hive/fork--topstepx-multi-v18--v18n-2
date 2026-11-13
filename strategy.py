"""v18n-2 experiment 68.
FAMILY: nasdaq_quiet_session_reversal
Mechanism: a quiet Nasdaq session indicates suppressed dealer gamma and deferred rebalancing;
next-session flow reverses the prior small directional move.
Hypothesis: after completed bottom-decile 120-session NQ range, trade opposite its direction
next 17:00 CT through 15:00 CT, $250 stop. Falsification: stressed PnL, era, or yearly failure.
"""
import numpy as np
FAMILY="nasdaq_quiet_session_reversal";PARAMS={"quantile":.1,"lookback_sessions":120,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];o=ans['NQ'];c,t,h,l=d.close.to_numpy(),d.ct_sec.to_numpy(),d.high.to_numpy(),d.low.to_numpy();days=list(d.groupby('session',sort=False).indices.values());rets=[];ranges=[]
 for ix in days:
  side=0
  if len(ranges)>=120 and ranges[-1]<=np.quantile(ranges[-120:],.1):side=-int(np.sign(rets[-1]))
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if side and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if side*(c[i]-ref)<=-12.5:break
    o[i]=side
  rets.append(c[ix[-1]]/c[ix[0]]-1);ranges.append(h[ix].max()-l[ix].min())
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='NQ' else 0.) for s,d in panel.items()}
