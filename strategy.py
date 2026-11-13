"""v18n-2 experiment 144.
FAMILY: equity_lunch_breadth_execution_40day
Mechanism: aligned exceptional lunch moves across indexes reveal institutional execution that
continues into closing liquidity. Forty completed sessions provide causal seasonal context and
increase early-history coverage.
Hypothesis: two-index aligned top-5% 11:00-12:00 move, follow 12:01-15:00; $250 stops.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="equity_lunch_breadth_execution_40day";PARAMS={"lookback_sessions":40,"quantile":.95,"quorum":2}
STOP={'ES':5.,'NQ':12.5,'YM':50.,'RTY':5.}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()};info={}
 for s,d in panel.items():
  c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
  for day,ix in d.groupby('session',sort=False).indices.items():
   pre=[i for i in ix if 39600<=t[i]<43200]
   if len(pre)>1:
    m=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-40:]),.95) if len(hist)>=40 else np.inf
    if abs(m)>=th:info.setdefault(str(day),{})[s]=np.sign(m)
    hist.append(m)
 for s,d in panel.items():
  c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans[s]
  for day,ix in d.groupby('session',sort=False).indices.items():
   z=info.get(str(day),{});side=z.get(s,0)
   if not side or sum(v==side for v in z.values())<2:continue
   bars=[i for i in ix if 43260<=t[i]<54000]
   if not bars:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-STOP[s]:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.) for s,d in panel.items()}
