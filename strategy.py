"""v18n-2 experiment 94.
FAMILY: silver_prior_extreme_us_afternoon_reversal
Mechanism: an extreme completed COMEX-morning silver move leaves inventory imbalance that mean
reverts in next US afternoon as commercial liquidity returns.
Hypothesis: fade prior completed 08:30-09:30 top-5% SI shock from 11:00-15:00, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
FAMILY="silver_prior_extreme_us_afternoon_reversal";PARAMS={"lookback_days":120,"quantile":.95,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];o=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();days=list(d.groupby('session',sort=False).indices.values());hist=[]
 for ix in days:
  pre=[i for i in ix if 30600<=t[i]<34200];bars=[i for i in ix if 39600<=t[i]<54000]
  if pre and bars and len(hist)>=PARAMS['lookback_days']:
   prev=hist[-1];th=np.quantile([abs(x)for x in hist[-PARAMS['lookback_days']:]],PARAMS['quantile'])
   if abs(prev)>th:
    side=-np.sign(prev);ref=c[bars[0]]
    for i in bars[1:]:
     if side*(c[i]-ref)<=-.5:break
     o[i]=side
  if pre:hist.append(c[pre[-1]]/c[pre[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='SI' else 0.) for s,d in panel.items()}
