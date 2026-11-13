"""v18n-2 experiment 130.
FAMILY: heatingoil_crude_midmorning_refinery_flow
Mechanism: exceptional 09:30-10:30 heating-oil repricing reveals refinery hedge pressure that
passes through the refined-products complex and continues crude execution into settlement.
Hypothesis: follow CL after causal HO top-quintile move, 10:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="heatingoil_crude_midmorning_refinery_flow";PARAMS={"lookback_sessions":60,"quantile":.80,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'HO','CL'}<=set(panel):return ans
 d=panel['HO'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[];events={}
 for day,ix in d.groupby('session',sort=False).indices.items():
  pre=[i for i in ix if 34200<=t[i]<37800]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.80) if len(hist)>=60 else np.inf
   if abs(move)>=th:events[str(day)]=np.sign(move)
   hist.append(move)
 d=panel['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans['CL']
 for day,ix in d.groupby('session',sort=False).indices.items():
  side=events.get(str(day),0);bars=[i for i in ix if 37860<=t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.25:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='CL' else 0.) for s,d in panel.items()}
