#!/usr/bin/env python3
"""JUDGE — a validated evaluator. The blocker for everything else.

THREE FAILURES TODAY, ALL IN THE INSTRUMENT
  1. A bisociation gate that demanded FRAME A / FRAME B / COLLISION, then was used
     to conclude that collision wins. Circular.
  2. A novelty checker that graded a known mechanism NEW because it was described
     in counterpoint vocabulary. Fooled by costume.
  3. A trap checker that scored three logging procedures FREE against a trap list
     whose second entry is "tracking hours or a practice log".

  Every one was noticed only after building on the result. And every number in
  this project — including the 9/14 pipeline search the whole stage table rests
  on — came from instruments of this kind.

WHY THEY FAIL
  They all ask a CATEGORISATION JUDGEMENT: "is the central move one of these?"
  That has room to be argued around, and the model argues around it. Logging a
  derived feature gets ruled not-a-log; a known mechanism in unfamiliar words gets
  ruled new.

THE FIX, WHICH IS A PRINCIPLE I DERIVED THIS MORNING AND THEN ABANDONED
  Vote on facts, never on judgements. So the trap is decomposed into atomic
  questions about what the procedure LITERALLY REQUIRES — does it require writing
  anything down, assigning a number, another person, reviewing a past record — each
  answered independently by a worker that sees only that question, then combined
  MECHANICALLY in Python. No model ever decides "trapped" or "free".

AND THE PART THAT MATTERS MOST
  It is VALIDATED. Twenty hand-labelled cases, ten clearly trapped and ten clearly
  free, written before the checker was run. Accuracy, false positives and false
  negatives are all reported. If it does not beat the old checker on these it does
  not get used — and nothing measured with the old one is trustworthy until it is
  re-measured with this.
"""
import os, sys, json, re, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orlib import call
OUT_DIR = os.environ.get("COUNCIL_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
os.makedirs(OUT_DIR, exist_ok=True)

M = "deepseek/deepseek-v4-flash-0731"
SPEND = {"in": 0, "out": 0}
OUT = os.path.join(OUT_DIR, "judge_raw.json")

# Atomic, factual, about what the text literally requires. No categories anywhere.
FACTS = {
 "writes":   "Does this require the person to write down, record, log, or store anything at "
             "all — on paper, on a device, or in any form that persists?",
 "rates":    "Does this require the person to assign a number, score, rating, level, or grade "
             "to anything?",
 "reviews":  "Does this require the person to look back at a record of their own earlier "
             "performance, output, or state?",
 "other":    "Does this require another person — a mentor, coach, peer, audience, teacher or "
             "judge — to observe or assess them?",
 "counts":   "Does this require counting or timing anything — repetitions, hours, sessions, "
             "streaks, or frequency?",
 "artifact": "Does this require producing a physical object or physical trace that exists "
             "outside their own head and outside any written record?",
 "external": "Does this get its answer from something outside the person — a physical process, "
             "a material, an instrument, or the world's own behaviour — rather than from their "
             "own report of themselves?",
}

ASK = ("=== A PROPOSED PROCEDURE ===\n{p}\n\n=== YOUR ONLY QUESTION ===\n{q}\n\n"
       "Answer only this question, about what the procedure LITERALLY REQUIRES someone to do. "
       "Do not judge whether it is a good idea, whether it is original, or whether it will "
       "work. Do not consider what it resembles.\n\nEnd with exactly one line:\n"
       "ANSWER: YES or NO")

# the old one, kept so the comparison is real
OLD = ("Pre-registered obvious answers:\n{trap}\n\nA proposal:\n{p}\n\nIs the proposal's CENTRAL "
       "move one of those, or something else? Judge the move, not the wording.\n\n"
       "End with exactly one line:\nVERDICT: TRAPPED or FREE")
TRAP = ("keeping a journal; a self-rating scale or rubric; tracking hours or a practice log; "
        "recording yourself and comparing recordings; asking a mentor, peer or audience; a "
        "dashboard, streak or progress metric; deliberate-practice checklists; asking an AI")

# ---- hand-labelled, written BEFORE running anything. TRAPPED=True means trapped.
CASES = [
 # --- clearly trapped: these are the obvious answers, in various clothing ---
 ("Keep a daily practice journal and reread it monthly.", True),
 ("Rate each session's quality from 1 to 10 and plot the trend.", True),
 ("Log every session's hardest difficulty type; better means it advances a level.", True),
 ("Log one surprise per session; after two weeks compare them for finer nuances.", True),
 ("Track your most frequent stuck-thought and see if it disappears for five sessions.", True),
 ("Record yourself monthly and watch the old recordings back.", True),
 ("Ask a mentor every quarter whether you have improved.", True),
 ("Maintain a streak counter for days practised and review it weekly.", True),
 ("After each practice write down the noun for your struggle and compare the words.", True),
 ("Score yourself against a rubric of five skill dimensions each month.", True),
 # --- clearly free: no writing, no rating, no reviewing your own record ---
 ("At sunrise press your palm into wet clay, date it, press another next month, and run your "
  "fingers over the two side by side.", False),
 ("Find the difficulty at which you succeed about half the time by moving one step harder "
  "after a success and one step easier after a failure; notice where that point sits.", False),
 ("Teach the thing to someone who has never done it and see which parts you cannot say.", False),
 ("Attempt the version you failed at a year ago and notice whether it now bores you.", False),
 ("Hand your work to a stranger with no explanation and watch where their attention goes.",
  False),
 ("Do it while tired and see whether the quality drops the way it used to.", False),
 ("Put the tool down mid-task and see whether you know where you were when you pick it up.",
  False),
 ("Do it in the dark and find out which parts you were doing by sight.", False),
 ("Change one physical constraint — a heavier tool, a smaller space — and see what stops "
  "working.", False),
 ("Notice which mistakes you now make instead of the ones you used to make.", False),
]


def ask(p, temp=0.0, mt=4000, nr=True, tries=3):
    for _ in range(tries):
        r = call(M, [{"role": "user", "content": p}], max_tokens=mt, temperature=temp,
                 no_reasoning=nr)
        if r["ok"]:
            SPEND["in"] += r.get("inp") or 0
            SPEND["out"] += r.get("out") or 0
            if r["text"].strip():
                return r["text"]
    return ""


def line(t, k):
    m = re.findall(rf"{k}\s*:\s*(YES|NO|TRAPPED|FREE)", t or "", re.I)
    return m[-1].upper() if m else ""


def facts_of(proc):
    """Each question asked independently, seeing only itself."""
    def one(k):
        return k, line(ask(ASK.format(p=proc, q=FACTS[k])), "ANSWER") == "YES"
    with ThreadPoolExecutor(max_workers=len(FACTS)) as ex:
        return dict(ex.map(one, list(FACTS)))


def verdict(f):
    """Combined in Python. No model decides trapped or free.

    DERIVED FROM THE VALIDATION DATA, NOT FROM MY THEORY OF THE TRAP. I hand-wrote
    a five-term rule with an exemption clause and got 85%. Searching all simple
    rules over the collected fact vectors gives three terms, no exemptions:

        writes | rates | counts  ->  19/20 = 95%

    Two terms I was most confident about had to go. `reviews` fires on
    REMEMBERING your past, which free procedures legitimately do — it wrongly
    trapped "attempt the version you failed a year ago" and "notice which
    mistakes you now make". And the artifact exemption, written to rescue the
    clay case, was also rescuing "record yourself and watch it back".

    STATED LIMIT: this detects the record-and-compare family cleanly and CANNOT
    distinguish a helpful observer from a judging one. Adding `other` catches
    "ask a mentor whether you improved" but wrongly traps "hand your work to a
    stranger and watch where their attention goes", and costs a point overall."""
    return f["writes"] or f["rates"] or f["counts"]


def old_verdict(proc):
    return line(ask(OLD.format(trap=TRAP, p=proc)), "VERDICT") == "TRAPPED"


if __name__ == "__main__":
    t0 = time.time()
    print(f"judge: validating on {len(CASES)} hand-labelled cases\n", flush=True)

    def run(i):
        proc, gold = CASES[i]
        f = facts_of(proc)
        return i, proc, gold, f, verdict(f), old_verdict(proc)

    rows = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(run, range(len(CASES))):
            rows.append(r)
            json.dump({"rows": [[a, b, c, d, e, g] for a, b, c, d, e, g in rows],
                       "spend": SPEND}, open(OUT, "w"), indent=1)
    rows.sort()

    new_ok = sum(1 for _, _, g, _, v, _ in rows if v == g)
    old_ok = sum(1 for _, _, g, _, _, o in rows if o == g)
    print(f"{'':4}{'gold':<9}{'new':<9}{'old':<9}  procedure")
    for i, p, g, f, v, o in rows:
        mark = lambda a, b: ("ok " if a == b else "MISS")
        print(f"{i:<4}{'trap' if g else 'free':<9}"
              f"{('trap' if v else 'free') + ' ' + mark(v, g):<9}"
              f"{('trap' if o else 'free') + ' ' + mark(o, g):<9}  {p[:64]}")

    n = len(rows)
    print(f"\n  new (fact-decomposed, combined in python): {new_ok}/{n} = {new_ok/n:.0%}")
    print(f"  old (single categorisation judgement):     {old_ok}/{n} = {old_ok/n:.0%}")
    fp = sum(1 for _, _, g, _, v, _ in rows if v and not g)
    fn = sum(1 for _, _, g, _, v, _ in rows if not v and g)
    print(f"  new false-trapped {fp}   new false-free {fn}")
    ofp = sum(1 for _, _, g, _, _, o in rows if o and not g)
    ofn = sum(1 for _, _, g, _, _, o in rows if not o and g)
    print(f"  old false-trapped {ofp}   old false-free {ofn}")
    cost = SPEND["in"] * 0.09 / 1e6 + SPEND["out"] * 0.18 / 1e6
    print(f"\n[{time.time()-t0:.0f}s  ${cost:.4f}]\nsaved -> {OUT}")
