"""v18n-2 experiment 160.
FAMILY: yen_silver_us_safehaven_reversal
Mechanism: a sustained yen move signals safe-haven demand already absorbed during Asia; COMEX
silver reverses into US risk transfer rather than following the stale FX signal.
Hypothesis: fade completed 5-day 6J direction in SI 09:31-15:00; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="yen_silver_us_safehaven_reversal";PARAMS={"lookback_sessions":5,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'6J','SI'}<=set(panel):return ans
 j=panel['6J'];sj=[]
 for day,g in j.groupby('session',sort=False):sj.append((pd.Timestamp(day),g.close.iloc[-1]-g.close.iloc[0]))
 hist={};moves=[]
 for day,r in sj:
  hist[str(day.date())]=-np.sign(sum(moves[-5:])) if len(moves)>=5 else 0;moves.append(r)
 d=panel['SI'];out=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();day=pd.to_datetime(d.session).dt.strftime('%Y-%m-%d').to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  side=hist.get(day[ix[0]],0);bars=[i for i in ix if 34260<=t[i]<54000]
  if not side or not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if side*(c[i]-ref)<=-.5:break
   out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='SI' else 0.) for s,d in panel.items()}
