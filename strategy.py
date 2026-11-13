"""v18n-2 experiment 55.
FAMILY: nasdaq_month_end_rebalance_demand
Mechanism: month-end pension and target-date fund rebalancing concentrates Nasdaq futures demand
into final trading days before reporting cut-off.
Hypothesis: long NQ on final three business days from 17:00 CT reopen through 15:00 CT, $250
stop. Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="nasdaq_month_end_rebalance_demand";PARAMS={"trading_days":3,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'NQ' not in panel:return ans
 d=panel['NQ'];o=ans['NQ'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy(); days=list(d.groupby('session',sort=False).indices.values())
 for n,ix in enumerate(days):
  day=pd.Timestamp(d.session.iloc[ix[0]])
  # Session labels already carry business calendar; next three labels crossing month means last 3.
  future=[pd.Timestamp(d.session.iloc[z[0]]) for z in days[n+1:n+4]]
  if sum(x.month!=day.month for x in future)<1:continue
  bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
  if len(bars)<2:continue
  ref=c[bars[0]]
  for i in bars[1:]:
   if c[i]-ref<=-12.5:break
   o[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='NQ' else 0.) for s,d in panel.items()}
