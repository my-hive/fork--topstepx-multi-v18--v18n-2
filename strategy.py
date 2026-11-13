"""v18n-2 experiment 38.
FAMILY: treasury_extreme_gold_reversal
Mechanism: an extreme completed Treasury-note daily move can be an overshoot in macro
positioning; gold hedging flow reverses next session when rate shock stabilizes.
Hypothesis: trailing-300 top-5% absolute ZN close return, trade GC opposite direction next
session from 17:00 CT reopen through 15:00 CT, $250 stop. Falsification: stress/era/years.
"""
import numpy as np
FAMILY="treasury_extreme_gold_reversal"
PARAMS={"quantile":.95,"lookback_sessions":300,"stop_dollars":250}
def _sides(df):
 c,t=df.close.to_numpy(),df.ct_sec.to_numpy();prior=None;hist=[];out=[]
 for ix in df.groupby("session",sort=False).indices.values():
  end=[i for i in ix if 53400<=t[i]<=54000];side=0
  if end:
   px=c[end[-1]]
   if prior is not None:
    r=px/prior-1;past=np.abs(hist[-300:])
    if len(past)>=300 and abs(r)>=np.quantile(past,.95):side=-int(np.sign(r))
    hist.append(r)
   prior=px
  out.append(side)
 return out
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {"ZN","GC"}<={*panel}:return ans
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
