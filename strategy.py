"""v18n-2 experiment 123.
FAMILY: equity_index_lunch_breadth_zscore_quorum
Mechanism: aligned lunch repricing across >=2 US equity indices marks broad institutional execution
that continues into closing liquidity. Volatility-normalised trigger (z vs trailing 60-session std)
adapts to regime and fires earlier in sample than a 120-session percentile warm-up.
Hypothesis: follow quorum members 12:01-15:00 when |z|>=1.75; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure; exp120 comparison for year coverage.
"""
import numpy as np
import pandas as pd
FAMILY="equity_index_lunch_breadth_zscore_quorum";PARAMS={"lookback_sessions":60,"z_threshold":1.75,"quorum":2}
STOP={'ES':5.,'NQ':12.5,'YM':50.,'RTY':5.}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 info={}
 for s in panel:
  d=panel[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
  for day,ix in d.groupby('session',sort=False).indices.items():
   pre=[i for i in ix if 39600<=t[i]<43200]
   if len(pre)>1:
    m=c[pre[-1]]-c[pre[0]]
    if len(hist)>=60:
     sd=np.std(hist[-60:])
     if sd>0 and abs(m)>=1.75*sd:info.setdefault(str(day),{})[s]=np.sign(m)
    hist.append(m)
 for s in panel:
  d=panel[s];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans[s]
  for day,ix in d.groupby('session',sort=False).indices.items():
   z=info.get(str(day),{})
   if s not in z:continue
   side=z[s]
   if sum(v==side for v in z.values())<2:continue
   bars=[i for i in ix if 43260<=t[i]<54000]
   if not bars:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-STOP[s]:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250.) for s,d in panel.items()}
