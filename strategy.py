"""v18n-2 experiment 355.
FAMILY: equity_lunchbreadth_junerebalance_quarterlystocks_combination
Mechanism: broad lunch index execution and June NQ index-rebalance plus quarterly Grain Stocks repricing are distinct
calendar flows combined to raise combine-attempt frequency.
Hypothesis: causal 60-session two-index lunch quorum plus June NQ opening continuation; $250 stops.
Falsification: stressed PnL, era, years, or shared-account risk failure.
"""
import numpy as np
import pandas as pd
FAMILY="equity_lunchbreadth_junerebalance_quarterlystocks_combination";PARAMS={"lookback_sessions":60,"quantile":.95,"quorum":2,"stocks_start":40500}
STOP={'ES':5.,'NQ':12.5,'YM':50.,'RTY':5.,'ZS':1.0}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()};info={}
 for s,d in panel.items():
  if s not in STOP or s=="ZS":continue
  c,t=d.close.to_numpy(),d.ct_sec.to_numpy();hist=[]
  for day,ix in d.groupby('session',sort=False).indices.items():
   pre=[i for i in ix if 39600<=t[i]<43200]
   if len(pre)>1:
    m=c[pre[-1]]-c[pre[0]];th=np.quantile(np.abs(hist[-60:]),.95) if len(hist)>=60 else np.inf
    if abs(m)>=th:info.setdefault(str(day),{})[s]=np.sign(m)
    hist.append(m)
 for s,d in panel.items():
  if s not in STOP:continue
  c,t=d.close.to_numpy(),d.ct_sec.to_numpy();out=ans[s];mon=pd.to_datetime(d.session).dt.month.to_numpy()
  dom=pd.to_datetime(d.session).dt.day.to_numpy()
  for day,ix in d.groupby('session',sort=False).indices.items():
   if s=='ZS':
    side=1 if dom[ix[0]] in (30,31) else 0;bars=[i for i in ix if 40560<=t[i]<46800]
   else:
    z=info.get(str(day),{});side=z.get(s,0) if sum(v==z.get(s,0) for v in z.values())>=2 else 0;bars=[i for i in ix if 43260<=t[i]<54000]
    if s=='NQ' and mon[ix[0]]==6:
     pre=[i for i in ix if 30600<=t[i]<36000]
     if len(pre)>1: side=np.sign(c[pre[-1]]-c[pre[0]]);bars=[i for i in ix if 36000<=t[i]<54000]
   if not side or not bars:continue
   ref=c[bars[0]]
   for i in bars:
    if side*(c[i]-ref)<=-STOP[s]:break
    out[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s in STOP else 0.) for s,d in panel.items()}
