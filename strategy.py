"""v18n-2 experiment 142.
FAMILY: silver_european_morning_industrial_flow
Mechanism: European industrial and bullion-dealer order flow creates persistent silver buying
through late European morning before COMEX price discovery.
Hypothesis: long SI 06:00-08:30 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="silver_european_morning_industrial_flow";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'SI' not in panel:return ans
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  bars=[i for i in ix if 21600<=t[i]<30600]
  if not bars:continue
  ref=c[bars[0]];stopped=False
  for i in bars:
   if stopped:continue
   if c[i]-ref<=-.5:stopped=True
   else:out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
