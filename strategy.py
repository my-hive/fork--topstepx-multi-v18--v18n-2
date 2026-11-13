"""v18n-2 experiment 59.
FAMILY: gold_friday_prior_loss_shortcover
Mechanism: a Thursday gold loss leaves speculative short inventory that is covered into Friday
liquidity ahead of weekend event risk.
Hypothesis: after completed negative Thursday, long GC Friday 17:00 CT through 15:00 CT,
$250 stop. Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_friday_prior_loss_shortcover";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(); days=list(d.groupby('session',sort=False).indices.values());last=[]
 for n,ix in enumerate(days):
  day=pd.Timestamp(d.session.iloc[ix[0]]);side=day.dayofweek==4 and n and last[-1]<0
  # complete prior session close/open retained before processing current session
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if side and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if c[i]-ref<=-2.5:break
    o[i]=1
  last.append(c[ix[-1]]/c[ix[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
