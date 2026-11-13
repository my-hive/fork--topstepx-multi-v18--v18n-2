"""v18n-2 experiment 135.
FAMILY: longbond_gold_midmorning_realrate_flow
Mechanism: exceptional long-bond repricing during US macro execution reveals real-rate demand;
gold hedgers transmit same-direction safe-haven flow into COMEX settlement.
Hypothesis: follow GC after causal ZB top-30% 09:30-10:30 move, 10:31-15:00; one $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="longbond_gold_midmorning_realrate_flow";PARAMS={"lookback_sessions":60,"quantile":.70,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'ZB','GC'}<=set(panel):return ans
 d=panel['ZB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[];events={}
 for day,ix in d.groupby('session',sort=False).indices.items():
  pre=[i for i in ix if 34200<=t[i]<37800]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.70) if len(hist)>=60 else np.inf
   if abs(move)>=th:events[str(day)]=np.sign(move)
   hist.append(move)
 d=panel['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans['GC']
 for day,ix in d.groupby('session',sort=False).indices.items():
  side=events.get(str(day),0);bars=[i for i in ix if 37860<=t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if side*(c[i]-ref)<=-2.5:stopped=True
   else:out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
