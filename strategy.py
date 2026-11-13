"""v18n-2 experiment 310."""
import numpy as np
import pandas as pd
FAMILY="spx_fomc_proxy_repricing_continuation"
PARAMS={"reference_end":47700,"trade_start":47760,"trade_end":53100,"stop_dollars":250}
def signals(panel):
    ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
    if "ES" not in panel:return ans
    d=panel["ES"];c,t=d.close.to_numpy(),d.ct_sec.to_numpy();cal=pd.to_datetime(d.session);day,wd=cal.dt.day.to_numpy(),cal.dt.dayofweek.to_numpy();out=ans["ES"]
    for p in d.groupby("session",sort=False).indices.values():
        if not (wd[p[0]]==2 and 15<=day[p[0]]<=21):continue
        a=None;side=0
        for i in p:
            if t[i]==47700:a=c[i];side=1 if c[i]>=c[p[0]] else -1
            elif a is not None and 47760<=t[i]<53100:
                if side*(c[i]-a)<=-5:break
                out[i]=side
    return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="ES" else 0.0) for s,d in panel.items()}
