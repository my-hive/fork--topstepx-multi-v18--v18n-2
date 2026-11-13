"""v18n-2 experiment 39.
FAMILY: copper_london_range_us_breakout
Mechanism: London hours establish a copper inventory/industrial-information range; a US
COMEX break releases deferred hedger flow in same direction as US liquidity deepens.
Hypothesis: break prior completed 06:00-08:30 CT HG range after 08:30, trade breakout until
15:00; $250 stop. One trade per session. Falsification: stress/era/year failure.
"""
import numpy as np
FAMILY="copper_london_range_us_breakout"
PARAMS={"range_start":21600,"range_end":30600,"entry_start":30600,"exit_sec":54000,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'HG' not in panel:return ans
 d=panel['HG'];o=ans['HG'];c,h,l,t=d.close.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  rng=[i for i in ix if 21600<=t[i]<30600];e=[i for i in ix if 30600<=t[i]<54000]
  if not rng or not e:continue
  hi,lo=h[rng].max(),l[rng].min();side=0;ref=0.
  for i in e:
   if not side:
    if c[i]>hi:side,ref=1,c[i]
    elif c[i]<lo:side,ref=-1,c[i]
   if side:
    if side*(c[i]-ref)<=-.01:break
    o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='HG' else 0.) for s,d in panel.items()}
