import json,sys,hashlib,subprocess,re
# usage: log_exp.py report.json hypothesis [error]
r=json.load(open(sys.argv[1])); s=r['stressed']
rec=dict(agent='v18n-2',sha=r['strategy_sha256'],commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
 family=r['family']['tag'],symbols=r['symbols'],hypothesis=sys.argv[2],dev_score=s['dev_score'],worst_three_mean=s['worst_three_mean'],
 folds=s['folds'],year_fraction=s['positive_year_fraction'],eras={k:v['pnl'] for k,v in s['era_blocks'].items()},
 total_pnl=s['total_pnl'],max_entry_risk=s['max_entry_risk'],entry_div_share=s['entry_0830_0930_share'],eligible=s['eligibility']['passed'],checks=s['eligibility']['checks'],error=None)
open('experiments.jsonl','a').write(json.dumps(rec)+'\n'); print(json.dumps(rec)[:600])
