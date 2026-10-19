#!/usr/bin/env python3
"""COUNCIL — use the thing. The winning arm, pointed at a real question.

Everything else in this directory tests the machinery. This runs it.

The A/B settled the architecture: `B_ops` beat a plain call on 5/5 questions and beat the
graph on 4/5 (mean robustness 0.70 vs 0.35 and 0.40). It is also the simplest arm —
generate, then attack to exhaustion from assigned angles, keep the revision. No chains, no
edge classification, no claim graph.

Output ships with its scars, never with a self-assessment: the claim, how many assigned
attacks it held, what the surviving attacks were, what would falsify it, and what it
depends on. "This is strong work" has no falsifier, so it is not in the schema.

    ./council.py "your question"
"""
import os, sys, json, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
from engine import ask, harden, annotate, measure_trap, same, Terminal, P_MODE
OUT_DIR = os.environ.get("COUNCIL_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
os.makedirs(OUT_DIR, exist_ok=True)

OUT = os.path.join(OUT_DIR, "council_raw.json")

P_SEED = ("{q}\n\nAnswer directly and concretely. State the actual proposal or mechanism, "
          "not a survey of considerations. No preamble, no hedging, no summary of the "
          "problem back to me.{cond}")

# Decorrelated seeds. Not personas — personas buy vocabulary. These change what is
# structurally available: what may be assumed, what has already failed, what may be said.
SEEDS = {
 "plain":   "",
 "defeat":  "\n\nThe obvious answer here has already been tried and it failed for a reason "
            "nobody wrote down. Assume it is unavailable to you.",
 "foreign": "\n\nYou work on this class of problem in an unrelated technical field and have "
            "never studied the one it belongs to. Reason about it in your own terms.",
 "invert":  "\n\nBefore answering, name the thing everyone attempting this takes for granted, "
            "and then answer without it.",
}


def run(question, seeds=None, show_mode=True):
    t0 = time.time()
    seeds = seeds or list(SEEDS)

    mode = None
    if show_mode:
        print("measuring the modal answer (what to beat)...", flush=True)
        mode, sizes, _ = measure_trap(question)
        print(f"  mode [{'/'.join(map(str, sizes))}]: {(mode or '?')[:220]}\n", flush=True)

    print(f"generating {len(seeds)} decorrelated candidates, "
          f"then attacking each to exhaustion...\n", flush=True)
    with ThreadPoolExecutor(max_workers=len(seeds)) as ex:
        cands = list(ex.map(
            lambda s: ask(P_SEED.format(q=question, cond=SEEDS[s]), temp=1.0, mt=3000), seeds))

    with ThreadPoolExecutor(max_workers=len(seeds)) as ex:
        hard = list(ex.map(harden, [c for c in cands if c.strip()]))
    with ThreadPoolExecutor(max_workers=len(hard)) as ex:
        ann = list(ex.map(lambda h: annotate(h["claim"]), hard))
    for h, (fal, cond) in zip(hard, ann):
        h["falsifier"], h["conditional"] = fal, cond
        h["in_mode"] = same(h["claim"], mode) if mode else None

    hard.sort(key=lambda h: (-h["held"] / max(1, h["faced"]), -h["faced"]))
    json.dump({"question": question, "mode": mode, "results": hard,
               "spend": engine.SPEND}, open(OUT, "w"), indent=1)

    for i, h in enumerate(hard):
        print("=" * 84)
        print(f"[{h['held']}/{h['faced']} attacks held"
              f"{'' if h['in_mode'] is None else ('  · IN THE MODE' if h['in_mode'] else '  · outside the mode')}]")
        print(f"\n{h['claim']}\n")
        if h["falsifier"]:
            print(f"  falsified by: {h['falsifier']}")
        if h["conditional"]:
            print(f"  depends on:   {h['conditional']['var']}")
            print(f"     if high:   {h['conditional']['high'][:150]}")
            print(f"     if low:    {h['conditional']['low'][:150]}")
        landed = [s for s in h["scars"] if s["outcome"] in ("MOVED", "BROKE")]
        if landed:
            print(f"  attacks that landed and forced a change:")
            for s in landed:
                print(f"     - [{s['angle']}] {s['kill'][:150]}")
        print(flush=True)

    cost = engine.SPEND["in"] * 0.14 / 1e6 + engine.SPEND["out"] * 0.28 / 1e6
    print(f"[{time.time()-t0:.0f}s  {engine.SPEND['calls']} calls  ${cost:.4f}]  -> {OUT}")
    return hard


if __name__ == "__main__":
    q = " ".join(sys.argv[1:])
    if not q:
        print(__doc__); sys.exit(1)
    try:
        run(q)
    except Terminal as e:
        print(f"ABORTED (terminal API failure — output above is incomplete):\n  {str(e)[:200]}")
        sys.exit(1)
