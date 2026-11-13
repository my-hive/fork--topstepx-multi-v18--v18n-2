"""v18n-2 experiment 172.
FAMILY: gold_spring_physical_inventory_reversal
Mechanism: completed March-May Asian gold accumulation and mine-hedging flow reverses when US
COMEX liquidity absorbs the seasonal physical inventory pressure.
Hypothesis: fade completed prior-session Asian GC move during spring 08:30-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_spring_physical_inventory_reversal";PARAMS={"months":[3,4,5],"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];out=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();mo=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 21600<=t[i]<30600];bars=[i for i in ix if 30600<=t[i]<54000]
  if mo[ix[0]] not in {3,4,5} or len(x)<2 or not bars:continue
  side=-np.sign(c[x[-1]]-c[x[0]]);ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-2.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='GC' else 0.) for s,d in panel.items()}
