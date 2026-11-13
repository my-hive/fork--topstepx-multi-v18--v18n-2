"""v18n-2 experiment 88.
FAMILY: copper_intraday_extreme_shock_continuation
Mechanism: extreme 30-minute copper shocks reveal order-flow information that continues while
industrial hedgers and liquidity providers adjust quotes.
Hypothesis: follow causal top-5% 30-minute HG shock for next 30 minutes, $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
FAMILY="copper_intraday_extreme_shock_continuation";PARAMS={"lookback_bars":7200,"quantile":.95,"hold_bars":30,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];o=ans['HG'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[];end=-1;side=0;ref=0.
 for i in range(30,len(d)):
  if i>end and len(hist)>=PARAMS['lookback_bars'] and t[i]%1800==0:
   r=c[i-1]/c[i-30]-1;th=np.quantile(hist[-PARAMS['lookback_bars']:],PARAMS['quantile'])
   if abs(r)>th:side=int(np.sign(r));end=i+PARAMS['hold_bars'];ref=c[i]
  hist.append(abs(c[i-1]/c[i-30]-1))
  if i<=end and side:
   if side*(c[i]-ref)<=-.01: end=i;side=0
   else:o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='HG' else 0.) for s,d in panel.items()}
