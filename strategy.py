"""v18n-2 experiment 27. Independent metals family.
FAMILY: copper_us_open_volume_anomaly_reversal
Mechanism: abnormal copper volume during completed first US hour can exhaust an inventory/
industrial-news liquidity shock; afternoon reverts the opening directional overshoot.
Hypothesis: top-5% 08:30-09:30 HG volume vs prior 60 sessions, fade hour direction
09:31->15:00, $250 stop. Falsification: stressed loss or negative era.
"""
import numpy as np
FAMILY="copper_us_open_volume_anomaly_reversal";PARAMS={"q":.95,"n":60,"entry":34260,"exit":54000,"stop":250}
def signals(panel):
 a={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "HG" not in panel:return a
 d=panel["HG"];o=a["HG"];c,v,t=d.close.to_numpy(),d.volume.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby("session",sort=False).indices.values():
  h=[i for i in ix if 30600<=t[i]<34200];e=[i for i in ix if PARAMS["entry"]<=t[i]<PARAMS["exit"]]
  if not h:continue
  vol=v[h].sum();past=hist[-60:]
  if len(past)>=60 and vol>=np.quantile(past,.95) and e:
   side,ref=-int(np.sign(c[h[-1]]-c[h[0]])),c[e[0]]
   for i in e:
    if side*(c[i]-ref)<=-.01:break
    o[i]=side
  hist.append(vol)
 return a
def entry_risk(panel):return {s:np.full(len(d),290. if s=="HG" else 0.) for s,d in panel.items()}
