"""v18n-2 experiment 47.
FAMILY: gold_silver_daily_divergence_reversion
Mechanism: an extreme daily GC-vs-SI return divergence is temporary relative-value flow;
gold mean-reverts as precious-metal substitutes rebalance following session.
Hypothesis: prior completed return divergence top decile vs trailing 120, fade GC direction
next reopen through 15:00 CT, $250 stop. Falsification: stressed/era/year failure.
"""
import numpy as np
FAMILY="gold_silver_daily_divergence_reversion";PARAMS={"quantile":.9,"lookback_sessions":120,"stop_dollars":250}
def _closes(d):
 c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=[]
 for ix in d.groupby('session',sort=False).indices.values():
  z=[i for i in ix if 53400<=t[i]<=54000];out.append(c[z[-1]] if z else np.nan)
 return out
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'GC','SI'}<=set(panel):return ans
 a,b=_closes(panel['GC']),_closes(panel['SI']);pending=[];hist=[]
 for n in range(len(a)):
  side=0
  if n>=1 and not np.isnan(a[n]) and not np.isnan(b[n]) and not np.isnan(a[n-1]) and not np.isnan(b[n-1]):
   div=a[n]/a[n-1]-b[n]/b[n-1];past=np.abs(hist[-120:])
   if len(past)>=120 and abs(div)>=np.quantile(past,.9):side=-int(np.sign(div))
   hist.append(div)
  pending.append(side)
 d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for n,ix in enumerate(d.groupby('session',sort=False).indices.values()):
  side=pending[n-1] if n else 0;bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if not side or len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if side*(c[i]-ref)<=-2.5:break
   o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
