"""v18n-2 experiment 49.
FAMILY: euro_london_shock_silver_continuation
Mechanism: extreme completed London EUR futures moves are monetary-dollar information shocks;
silver continues direction during COMEX liquidity window.
Hypothesis: 6E 02:00-08:30 CT return top 5% absolute vs trailing 120 sessions, trade SI same
direction 08:30-15:00 CT, $250 stop. Falsification: stressed/era/year failure.
"""
import numpy as np
FAMILY="euro_london_shock_silver_continuation";PARAMS={"quantile":.95,"lookback_sessions":120,"stop_dollars":250}
def _sides(df):
 c,t=df.close.to_numpy(),df.ct_sec.to_numpy();hist=[];out=[]
 for ix in df.groupby('session',sort=False).indices.values():
  x=[i for i in ix if 7200<=t[i]<30600];side=0
  if len(x)>1:
   r=c[x[-1]]/c[x[0]]-1;past=np.abs(hist[-120:])
   if len(past)>=120 and abs(r)>=np.quantile(past,.95):side=int(np.sign(r))
   hist.append(r)
  out.append(side)
 return out
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'6E','SI'}<=set(panel):return ans
 sides=_sides(panel['6E']);d=panel['SI'];o=ans['SI'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for n,ix in enumerate(d.groupby('session',sort=False).indices.values()):
  side=sides[n] if n<len(sides) else 0;e=[i for i in ix if 30600<=t[i]<54000]
  if not side or not e:continue
  ref=c[e[0]]
  for i in e:
   if side*(c[i]-ref)<=-.05:break
   o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='SI' else 0.) for s,d in panel.items()}
