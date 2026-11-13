"""v18n-2 experiment 150.
FAMILY: longbond_prior_session_equity_duration_flow
Mechanism: completed long-bond repricing transmits through duration-sensitive portfolio hedges into
next-session equity-index futures demand.
Hypothesis: follow prior ZB session direction in NQ from 17:00 to 15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="longbond_prior_session_equity_duration_flow";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZB' not in panel or 'NQ' not in panel:return ans
 z=panel['ZB'];zc,zt=z.close.to_numpy(),z.ct_sec.to_numpy();drive={}
 for day,ix in z.groupby('session',sort=False).indices.items():
  bars=[i for i in ix if zt[i]>=61200 or zt[i]<54000]
  if len(bars)>1:drive[str(day)]=np.sign(zc[bars[-1]]-zc[bars[0]])
 n=panel['NQ'];c,t=n.close.to_numpy(),n.ct_sec.to_numpy();out=ans['NQ'];days=list(n.groupby('session',sort=False).indices.items())
 for k,(day,ix) in enumerate(days):
  if not k:continue
  side=drive.get(str(days[k-1][0]),0)
  if not side:continue
  bars=[i for i in ix if t[i]>=61200 or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-12.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='NQ' else 0.) for s,d in panel.items()}
