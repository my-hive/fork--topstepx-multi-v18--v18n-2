"""v18n-2 experiment 309."""
import numpy as np
import pandas as pd
FAMILY = "wheat_usda_wasde_repricing_continuation"
PARAMS = {"reference_end":40500,"trade_start":40560,"trade_end":46800,"stop_dollars":250}
def signals(panel):
    ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
    if "ZW" not in panel:return ans
    d=panel["ZW"]; c,t=d.close.to_numpy(),d.ct_sec.to_numpy(); day=pd.to_datetime(d.session).dt.day.to_numpy(); out=ans["ZW"]
    for p in d.groupby("session",sort=False).indices.values():
        if not 9<=day[p[0]]<=13:continue
        a=None; side=0
        for i in p:
            if t[i]==40500:a=c[i];side=1 if c[i]>=c[p[0]] else -1
            elif a is not None and 40560<=t[i]<46800:
                if side*(c[i]-a)<=-0.125:break
                out[i]=side
    return ans
def entry_risk(panel):return {s:np.full(len(d),250.0 if s=="ZW" else 0.0) for s,d in panel.items()}
