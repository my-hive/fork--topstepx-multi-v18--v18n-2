"""v18n-2 experiment 40. Claimed feed #3999.
FAMILY: metals_crosssectional_relative_momentum
Mechanism: daily cross-metal relative winner/loser reflects industrial versus monetary
allocation; winner persistence is traded market-neutral next session.
Hypothesis: after completed GC/SI/HG session, long strongest return and short weakest from
next 17:00 reopen through 15:00 CT, $250 stop per leg. Falsification: stress/era/year fail.
"""
import numpy as np
FAMILY="metals_crosssectional_relative_momentum";PARAMS={"stop_dollars":250};PV={'GC':100.,'SI':5000.,'HG':25000.}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not set(PV)<=set(panel):return ans
 data={};groups={}
 for s in PV:
  d=panel[s];t=d.ct_sec.to_numpy();c=d.close.to_numpy();groups[s]=list(d.groupby('session',sort=False).indices.values());data[s]={}
  for ix in groups[s]:
   end=[i for i in ix if 53400<=t[i]<=54000]
   if end:data[s][d.session.iloc[ix[0]]]=c[end[-1]]
 common=sorted(set.intersection(*(set(data[s]) for s in PV)));pending={};prior={}
 for n,day in enumerate(common):
  vals={s:data[s][day] for s in PV}
  if len(prior)==3 and n+1<len(common):
   r={s:vals[s]/prior[s]-1 for s in PV};hi=max(r,key=r.get);lo=min(r,key=r.get);pending[common[n+1]]={s:(1 if s==hi else -1 if s==lo else 0) for s in PV}
  prior=vals
 for s,d in panel.items():
  if s not in PV:continue
  c,t=d.close.to_numpy(),d.ct_sec.to_numpy();o=ans[s]
  for ix in groups[s]:
   side=pending.get(d.session.iloc[ix[0]],{}).get(s,0);bars=[i for i in ix if 61200<=t[i]<61500]+[i for i in ix if 30600<=t[i]<54000]
   if not side or len(bars)<2:continue
   ref=c[bars[0]]
   for i in bars[1:]:
    if side*(c[i]-ref)<=-250/PV[s]:break
    o[i]=side
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s in PV else 0.) for s,d in panel.items()}
