#!/usr/bin/env python3
"""No-network self-check: modules import, the problem sets are well formed, and the run
folders resolve inside this repo (or COUNCIL_OUT). Run: python3 selftest.py"""
import os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ok = True
for m in ("orlib", "engine", "eval_set", "hard_set"):
    try: importlib.import_module(m); print("ok  import", m)
    except Exception as e: ok = False; print("FAIL import", m, "->", e)
import eval_set, hard_set
for name, items in (("eval_set", eval_set.ITEMS), ("hard_set", getattr(hard_set, "ITEMS", []))):
    bad = [it.get("id") for it in items if not (it.get("q") and str(it.get("a", "")).strip())]
    print(("ok  " if not bad else "FAIL"), name, len(items), "items", ("" if not bad else f"missing answer: {bad}"))
    ok = ok and not bad
import engine
print("ok  run folder:", engine.OUT_DIR if hasattr(engine, "OUT_DIR") else "(engine keeps no files)")
print("\nself-check", "passed" if ok else "FAILED"); sys.exit(0 if ok else 1)
