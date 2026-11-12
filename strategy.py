"""v18n-2 experiment 26. Claimed volatility regime family.
FAMILY: gold_volatility_breakout_reversal
Mechanism: an extreme completed GC daily move occurring in an unusually quiet trailing
volatility regime is hypothesized to be a positioning overreaction; next session reverses.
Hypothesis: top-5% past-300 abs return and trailing 60 median abs return in bottom 30% of
past 300, fade next session from 17:00 reopen to 15:00, $250 stop.
Falsification: stressed loss/negative era.
"""
import numpy as np
FAMILY="gold_volatility_breakout_reversal";PARAMS={"q_move":.95,"q_quiet":.3,"lookback":300,"vollook":60,"stop":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "GC" not in panel:return ans
 d=panel["GC"];o=ans["GC"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();prior=None;rets=[];pending=0
 for ix in d.groupby("session",sort=False).indices.values():
  bars=[i for i in ix if t[i]>=61200 and t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if pending and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if pending*(c[i]-ref)<=-2.5:break
    o[i]=pending
  pending=0;end=[i for i in ix if 53400<=t[i]<=54000]
  if not end:continue
  px=c[end[-1]]
  if prior is not None:
   r=px/prior-1;past=np.abs(rets[-300:])
   if len(past)>=300:
    med=np.median(np.abs(rets[-60:]));quiet=np.quantile(past,.3)
    if abs(r)>=np.quantile(past,.95) and med<=quiet:pending=-int(np.sign(r))
   rets.append(r)
  prior=px
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=="GC" else 0.) for s,d in panel.items()}
