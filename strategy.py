"""v18n-2 experiment 37.
FAMILY: euro_asia_shock_silver_continuation
Mechanism: an extreme completed Asia-session EUR/USD futures move reprices dollar exposure
before COMEX; silver continues same-direction as US metals liquidity opens.
Hypothesis: 6E Asia return absolute value top 5% vs prior 300 sessions, trade same direction
in SI from 08:30 CT through 15:00 CT, $250 stop. Falsification: stress/era/year failure.
"""
import numpy as np
FAMILY="euro_asia_shock_silver_continuation"
PARAMS={"quantile":.95,"lookback_sessions":300,"entry_sec":30600,"exit_sec":54000,"stop_dollars":250}

def _sides(df):
 c,t=df.close.to_numpy(),df.ct_sec.to_numpy();hist=[];out=[]
 for ix in df.groupby("session",sort=False).indices.values():
  x=[i for i in ix if t[i]>=61200 or t[i]<30600]
  if len(x)<2:out.append(0);continue
  r=c[x[-1]]/c[x[0]]-1;past=np.abs(hist[-300:]);out.append(int(np.sign(r)) if len(past)>=300 and abs(r)>=np.quantile(past,.95) else 0);hist.append(r)
 return out

def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {"SI","6E"}<={*panel}:return ans
 sides=_sides(panel["6E"]);d=panel["SI"];o=ans["SI"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for n,ix in enumerate(d.groupby("session",sort=False).indices.values()):
  side=sides[n] if n<len(sides) else 0;e=[i for i in ix if 30600<=t[i]<54000]
  if not side or not e:continue
  ref=c[e[0]]
  for i in e:
   if side*(c[i]-ref)<=-.05:break
   o[i]=side
 return ans

def entry_risk(panel):return {s:np.full(len(d),290. if s=="SI" else 0.) for s,d in panel.items()}
