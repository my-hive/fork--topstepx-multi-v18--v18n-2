"""v18n-2 experiment 44.
FAMILY: gold_january_allocator_demand
Mechanism: calendar-year portfolio allocation and physical hedge renewal create persistent
January gold demand. Calendar is known before each session, no price-fitted trigger.
Hypothesis: long GC every January session from 17:00 CT reopen through 15:00 CT, $250 stop.
Falsification: stressed PnL/any era negative or fewer than 70% positive years.
"""
import numpy as np
import pandas as pd
FAMILY="gold_january_allocator_demand";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();months=pd.to_datetime(d.session).dt.month.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if months[ix[0]]!=1:continue
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref<=-2.5:break
   o[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
