"""v18n-2 experiment 148.
FAMILY: gasoline_comex_opening_inventory_reversal
Mechanism: an exceptional refined-product move during the US pre-release window is absorbed and
reversed by physical inventory hedgers after regular energy liquidity opens.
Hypothesis: fade RB top-decile 08:30-09:30 move, 09:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gasoline_comex_opening_inventory_reversal";PARAMS={"lookback_sessions":60,"quantile":.9,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'RB' not in panel:return ans
 d=panel['RB'];out=ans['RB'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for _,ix in d.groupby('session',sort=False).indices.items():
  pre=[i for i in ix if 30600<=t[i]<34200]
  if len(pre)>1:
   move=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.9) if len(hist)>=60 else np.inf;hist.append(move)
   if abs(move)<th:continue
   side=-np.sign(move);bars=[i for i in ix if 34260<=t[i]<54000]
   if not bars:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-.006:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='RB' else 0.) for s,d in panel.items()}
