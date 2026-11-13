"""v18n-2 experiment 57.
FAMILY: nasdaq_nonquarter_monthend_rebalance
Mechanism: non-quarter month-end target-date and retirement-fund rebalances create predictable
Nasdaq demand without quarter-end index/event noise.
Hypothesis: long NQ final three business days of non-quarter months from 17:00 CT through
15:00 CT, $250 stop. Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="nasdaq_nonquarter_monthend_rebalance";PARAMS={"trading_days":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];o=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  day=pd.Timestamp(d.session.iloc[ix[0]])
  if day.month in (3,6,9,12) or (day+pd.offsets.BDay(3)).month==day.month:continue
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref<=-12.5:break
   o[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='NQ' else 0.) for s,d in panel.items()}
