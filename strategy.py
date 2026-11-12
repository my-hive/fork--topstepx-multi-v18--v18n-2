"""v18n-2 experiment 25. Claimed volume family reversal.
FAMILY: silver_volume_anomaly_reversal
Mechanism: high overnight SI volume with directional move can exhaust information flow
before US liquidity, causing afternoon reversal as liquidity normalizes.
Hypothesis: top-5% trailing-60 overnight volume, fade overnight direction 09:35->15:00,
$250 stop. Falsification: stressed loss or negative era.
"""
import numpy as np
FAMILY="silver_volume_anomaly_reversal"
PARAMS={"quantile":.95,"lookback_sessions":60,"entry_sec":34500,"exit_sec":54000,"stop_dollars":250}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if "SI" not in panel:return ans
 d=panel["SI"];out=ans["SI"];c,v,t=d.close.to_numpy(),d.volume.to_numpy(),d.ct_sec.to_numpy();hist=[]
 for ix in d.groupby("session",sort=False).indices.values():
  pre=[i for i in ix if t[i]>=61200 or t[i]<30600];ent=[i for i in ix if PARAMS["entry_sec"]<=t[i]<PARAMS["exit_sec"]]
  if len(pre)<2:continue
  volume=v[pre].sum();past=hist[-60:]
  if len(past)>=60 and volume>=np.quantile(past,.95) and ent:
   side,ref=-int(np.sign(c[pre[-1]]-c[pre[0]])),c[ent[0]]
   for i in ent:
    if side*(c[i]-ref)<=-PARAMS["stop_dollars"]/5000:break
    out[i]=side
  hist.append(volume)
 return ans
def entry_risk(panel):return {s:np.full(len(d),290. if s=="SI" else 0.) for s,d in panel.items()}
