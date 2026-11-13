"""v18n-2 experiment 64.
FAMILY: gold_wednesday_comex_liquidity_reversal
Mechanism: midweek COMEX liquidity absorbs one-sided Asia/Europe hedge flow; intraday dealer
inventory normalization favors a short gold day session.
Hypothesis: short GC Wednesday 08:30-15:00 CT, $250 stop. Falsification: stressed PnL, era,
or yearly robustness failure.
"""
import numpy as np
import pandas as pd
FAMILY="gold_wednesday_comex_liquidity_reversal";PARAMS={"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'GC' not in panel:return ans
 d=panel['GC'];o=ans['GC'];c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
 for ix in d.groupby('session',sort=False).indices.values():
  if pd.Timestamp(d.session.iloc[ix[0]]).dayofweek!=2:continue
  bars=[i for i in ix if 30600<=t[i]<54000]
  if not bars:continue
  ref=c[bars[0]]
  for i in bars:
   if ref-c[i]<=-2.5:break
   o[i]=-1
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=='GC' else 0.) for s,d in panel.items()}
