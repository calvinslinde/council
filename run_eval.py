#!/usr/bin/env python3
import json, re, sys, os, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orlib import call
from eval_set import ITEMS
OUT_DIR = os.environ.get("COUNCIL_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
os.makedirs(OUT_DIR, exist_ok=True)

MODELS = [
 "nvidia/nemotron-3-ultra-550b-a55b:free",
 "nvidia/nemotron-3-nano-30b-a3b:free",
 "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
 "nvidia/nemotron-nano-9b-v2:free",
 "inclusionai/ling-3.0-flash:free",
 "poolside/laguna-s-2.1:free",
 "poolside/laguna-xs-2.1:free",
 "google/gemma-4-26b-a4b-it:free",
 "cohere/north-mini-code:free",
 "openai/gpt-oss-20b:free",
]
SUFFIX = "\n\nThink first if you need to, then end your reply with exactly:\nFINAL: <answer>"

def norm(s):
    s = s.strip().lower().replace("$","").replace(",","").rstrip(".")
    s = re.sub(r"\s+","",s)
    if re.fullmatch(r"\d+\.0+", s): s = s.split(".")[0]
    return s

def grade(txt, gold):
    m = re.findall(r"final\s*:\s*(.+)", txt, re.I)
    got = m[-1] if m else (txt.strip().splitlines() or [""])[-1]
    return norm(got) == norm(gold), got.strip()[:40]

def one(job):
    model, it = job
    r = call(model, [{"role":"user","content": it["q"]+SUFFIX}], max_tokens=6000)
    if not r["ok"]: return dict(model=model, id=it["id"], ok=False, corr=False, got=r["err"][:40], t=r["t"], out=0)
    c, got = grade(r["text"], it["a"])
    return dict(model=model, id=it["id"], ok=True, corr=c, got=got, t=r["t"], out=r["out"] or 0,
                empty=(r["text"]=="" ), finish=r["finish"])

jobs=[(m,it) for m in MODELS for it in ITEMS]
with ThreadPoolExecutor(max_workers=5) as ex:
    res=list(ex.map(one, jobs))
json.dump(res, open(os.path.join(OUT_DIR, "eval_raw.json"),"w"), indent=1)

print(f"{'model':<52} {'score':>6} {'avg_s':>7} {'avg_out':>8} {'empty':>6}")
for m in MODELS:
    rs=[r for r in res if r["model"]==m]
    sc=sum(r["corr"] for r in rs); n=len(rs)
    print(f"{m:<52} {sc}/{n:<4} {sum(r['t'] for r in rs)/n:7.1f} {sum(r['out'] for r in rs)/n:8.0f} {sum(1 for r in rs if r.get('empty')):>6}")
print()
for it in ITEMS:
    rs=[r for r in res if r["id"]==it["id"]]
    print(f"{it['id']:<8} gold={it['a']:<8} correct={sum(r['corr'] for r in rs)}/{len(rs)}   got: {[r['got'][:14] for r in rs if not r['corr']][:5]}")
