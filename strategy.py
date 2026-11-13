"""v18n-2 experiment 50.
FAMILY: treasury_extreme_gold_continuation
Mechanism: exceptional completed Treasury-note move reprices real-rate expectations; gold
continues with rate shock in following global session.
Hypothesis: completed ZN return top decile absolute vs trailing 120, follow its sign in GC
from next 17:00 CT reopen through 15:00 CT, $250 stop. Falsification: stress/era/year fail.
"""
import numpy as np
FAMILY="treasury_extreme_gold_continuation";PARAMS={"quantile":.9,"lookback_sessions":120,"stop_dollars":250}
def _sides(df):
 c,t=df.close.to_numpy(),df.ct_sec.to_numpy();last=[];hist=[];out=[]
 for ix in df.groupby('session',sort=False).indices.values():
  z=[i for i in ix if 53400<=t[i]<=54000];side=0
  if z:
   px=c[z[-1]]
   if last:
    r=px/last[-1]-1;past=np.abs(hist[-120:])
    if len(past)>=120 and abs(r)>=np.quantile(past,.9):side=int(np.sign(r))
    hist.append(r)
   last.append(px)
  out.append(side)
 return out
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'ZN','GC'}<=set(panel):return ans
 sides=_sides(panel['ZN']);d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for n,ix in enumerate(d.groupby('session',sort=False).indices.values()):
  side=sides[n-1] if n else 0;bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if not side or len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if side*(c[i]-ref)<=-2.5:break
   o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
