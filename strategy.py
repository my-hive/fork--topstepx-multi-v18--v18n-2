"""v18n-2 experiment 36.
FAMILY: gold_friday_after_loss_shortcover
Mechanism: a Thursday loss leaves speculative gold shorts vulnerable to Friday short
covering before weekend headline risk; only completed negative prior session activates.
Hypothesis: after negative completed GC Thursday, long following Friday session from 17:00
CT reopen through 15:00 CT, $250 stop. Falsification: stressed loss/negative era/years.
"""
import numpy as np
import pandas as pd
FAMILY="gold_friday_after_loss_shortcover"
PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "GC" not in panel:return ans
 d=panel["GC"];o=ans["GC"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();prior=None;weak=False
 for ix in d.groupby("session",sort=False).indices.values():
  day=pd.Timestamp(d.session.iloc[ix[0]]).dayofweek
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if weak and day==4 and len(bars)>1:
   ref=c[bars[0]]
   for i in bars[1:]:
    if c[i]-ref<=-2.5:break
    o[i]=1
  end=[i for i in ix if 53400<=t[i]<=54000]
  if end:
   px=c[end[-1]];weak=prior is not None and px<prior;prior=px
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=="GC" else 0.) for s,d in panel.items()}
