"""v18n-2 experiment 67.
FAMILY: crude_extreme_session_reversal
Mechanism: extreme completed crude session moves are inventory/liquidity overshoots that reverse
as next-session physical participants provide liquidity.
Hypothesis: bottom 5% trailing-120-session absolute CL return, take opposite side next session
17:00 CT-15:00 CT, $250 stop. Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
FAMILY="crude_extreme_session_reversal";PARAMS={"quantile":.95,"lookback_sessions":120,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' not in panel:return ans
 d=panel['CL'];o=ans['CL'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();days=list(d.groupby('session',sort=False).indices.values());rets=[]
 for ix in days:
  side=0
  if len(rets)>=120 and abs(rets[-1])>=np.quantile(np.abs(rets[-120:]),.95):side=-int(np.sign(rets[-1]))
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if side and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if side*(c[i]-ref)<=-.25:break
    o[i]=side
  rets.append(c[ix[-1]]/c[ix[0]]-1)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='CL' else 0.) for s,d in panel.items()}
