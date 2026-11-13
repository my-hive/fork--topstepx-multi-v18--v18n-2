"""v18n-2 experiment 125.
FAMILY: spx_monthly_payroll_flow
Mechanism: early-month payroll and systematic allocation flow creates persistent US equity demand
near calendar day six, after month-start portfolio positioning.
Hypothesis: long ES calendar-day-six session 17:00-15:00 CT; $250 stop.
Falsification: stressed PnL, era, or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="spx_monthly_payroll_flow";PARAMS={"calendar_day":6,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ES' not in panel:return ans
 d=panel['ES'];out=ans['ES'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();dom=pd.to_datetime(d.session).dt.day.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if dom[ix[0]]!=6:continue
  bars=[i for i in ix if 61200<=t[i] or t[i]<54000]
  if not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if c[i]-ref<=-5:break
   out[i]=1
 return ans
def entry_risk(panel):return {s:np.full(len(d),250. if s=='ES' else 0.) for s,d in panel.items()}
