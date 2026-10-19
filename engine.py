#!/usr/bin/env python3
"""ENGINE — the pieces, assembled. Persistent claim graph + exhaustion-terminated search.

WHAT CHANGED FROM THE PILE OF EXPERIMENTS

  1. THE GRAPH PERSISTS.  Every prior run was an isolated experiment whose result went
     into a markdown file that only I read. Multiplication factor 1. graph.jsonl is the
     multiplier: run N+1 is seeded by everything runs 1..N survived.

  2. NO FIXED N ANYWHERE.  Every constant in the old library was a "good enough" wearing
     a number — 8 draws, 5 angles, 7 cycles. Replaced by fixed points: each operator runs
     until it stops changing the state. This is self-budgeting, not unbounded: an easy
     step exhausts on the second draw, a hard one keeps going, so cost lands exactly where
     the difficulty is. The caps below are crash rails, not thresholds.

  3. THE TRAP FRAME IS MEASURED, NOT WRITTEN.  Every prior evaluator needed a hand-written
     trap per problem, which is why nothing generalised to an arbitrary question. But a
     trap frame is just THE MODAL ANSWER, and the mode is measurable: draw unscaffolded
     answers until saturation, cluster, take the largest cluster. That is apostatic's
     search image pointed at intake instead of at selection. Arbitrary questions now work.

  4. EDGE CLASSIFICATION IS TWO-AXIS.  web.py measured agreement only and got 100% on all
     six edges — zero resolution. The second axis was already in the data and unused:

            high agree + on-chain + not load-bearing  ->  NARRATION   (skip, free)
            high agree + on-chain + load-bearing      ->  FORCED      (accept, free)
            high agree + DIVERGED                     ->  DISPUTED    (spend here)
            low agree                                 ->  LEAP        (spend here)

     DISPUTED is the valuable cell: N decorrelated workers unanimously agree with each
     other and unanimously reject the step the chain took.

  5. CLUSTERING IS COMPLETE-LINKAGE.  Transitive closure merged A with C through B even
     when A and C were unrelated. That single bug produced the 100%s.

  6. NO SELF-EVALUATION IN THE SCHEMA.  A node ships claim, entailment, robustness, scars
     and falsifier. It never says how good it is. "This is strong work" has no falsifier,
     which makes it unfalsifiable output masquerading as content.

STILL UNSOLVED, STATED RATHER THAN PAPERED OVER
  - No external evidence channel. Everything here is model-internal, so the ceiling is
    "very well-examined belief", not "true". Retrieval is the next organ, not a polish pass.
  - Node identity is approximate. Merges are logged and reversible; they are not correct.
  - Where to cut a problem into steps is itself an inference and is not verified.
"""
import os, sys, json, re, time, itertools, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orlib import call
OUT_DIR = os.environ.get("COUNCIL_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
os.makedirs(OUT_DIR, exist_ok=True)

M = "deepseek/deepseek-v4-flash-0731"
STORE = os.path.join(OUT_DIR, "graph.jsonl")
SPEND = {"in": 0, "out": 0, "calls": 0}

# crash rails. not thresholds — the loops terminate on state change, these only stop runaway.
RAIL_DRAWS, RAIL_ROUNDS, RAIL_NODES = 30, 4, 400

# decorrelators. agreement between clones is not evidence, so every re-derivation runs
# under a different frame. this is the first job the condition library has ever had that
# is load-bearing: they are not generators here, they are variance sources.
CONDITIONS = {
 "plain":   "",
 "play":    "\n\nThis is play. Nothing here counts or will be checked. There is no correct "
            "answer to find and you are not being assessed.",
 "defeat":  "\n\nYour last three attempts at this were wrong, and wrong in the obvious way. "
            "Whatever first occurs to you has already failed.",
 "foreign": "\n\nYou work on this class of problem in an unrelated technical field and have "
            "never studied the one it belongs to. Reason about it in your own terms.",
 "strip":   "\n\nYou may not use any standard terminology from this field. Use only ordinary "
            "words for objects, flows, forces and quantities.",
 "defeat2": "\n\nThe obvious answer here has already been tried and it failed for a reason "
            "nobody has written down. Assume it is unavailable to you.",
}

P_MODE = ("{q}\n\nAnswer in two or three sentences. State the mechanism directly.{cond}")

P_CHAIN = ("{q}\n\nBuild the explanation as a numbered chain of steps, each a single "
           "declarative claim, each following from the one before. Six to eight steps. No "
           "preamble, no hedging, no summary.{cond}\n\n"
           "Format EXACTLY, one per line:\nSTEP 1: <claim>\nSTEP 2: <claim>")

P_NEXT = ("{q}\n\nSomeone reasoning about this has established the following, and nothing "
          "further:\n\n  {prior}\n\nWhat is the very next thing that follows? ONE claim. Not "
          "the final answer, not a summary — the single immediate next step.{cond}\n\n"
          "Answer with exactly one line:\nNEXT: <the one claim>")

# SELECTED BY MEASUREMENT, NOT WRITTEN. See samejudge.py — 44 hand-labelled pairs, 14
# single-judge variants and 546 combination rules. Every hand-reasoned prompt I wrote lost:
#
#   STRICT (was live in ab.py)   50%   over-split 22/25  -> every edge classified LEAP
#   PERMISSIVE (was in web.py)   80%   over-merge 8      -> 100% agreement on all six edges
#   EXTRACT (my "judge.py fix")  43%   never said SAME once
#   PERM_CAUSE / PERM_BOTH       64%   my targeted repairs, -22 points
#   PERM_SHOT (few-shot)         89%   best single judge
#
# The lesson in the numbers: STATING a rule makes the model over-apply it far past its
# scope; SHOWING examples encodes the boundary without giving it a rule to generalise.
#
# The winner is a COMBINATION — two judges, verdict computed in Python, which is the
# judge.py move I had not applied here. An OR can only over-merge where BOTH components
# over-merge, so it attacks the web.py failure mode (everything clusters, zero resolution)
# structurally rather than by tuning.
#
# STATED LIMIT: measured 93% on the label set, but that is the max over a 546-rule search
# on 44 cases and is selection-contaminated. Expect 89-91%. Its residual errors are
# over-splits across the vocabulary gap — the exact case decorrelated re-derivation
# depends on — so agreement numbers are biased slightly LOW, never high.
P_SAME_CORE = ("Two claims taken from explanations of the same phenomenon:\n\nA: {a}\n\nB: {b}"
               "\n\nDo A and B make the SAME causal move — assert the same thing causing the "
               "same thing?\n\nSay SAME if they describe one causal move, even in completely "
               "different vocabulary, even if one is more detailed or uses everyday words "
               "instead of technical ones.\nSay DIFFERENT if they are consecutive or separate "
               "steps in a chain (one causing the other), if one names a cause the other "
               "leaves out, or if they invoke different mechanisms.\n\n"
               "Answer one word: SAME or DIFFERENT")

P_SAME_SHOT = ("Decide whether two claims make the same causal move.\n\n"
               "Example 1:\nA: The pump pushes water uphill.\nB: The water is driven upward "
               "by the pump.\nSAME\n\n"
               "Example 2:\nA: The pipe bursts.\nB: The pipe bursts because the pressure "
               "exceeds its rating.\nDIFFERENT  (one is only the outcome, the other adds the "
               "cause)\n\n"
               "Example 3:\nA: The valve closes.\nB: With the valve shut, flow downstream "
               "stops.\nDIFFERENT  (consecutive steps, one causing the other)\n\n"
               "Example 4:\nA: Heat makes the metal expand.\nB: The bar gets longer when it "
               "warms up.\nSAME  (everyday wording, one mechanism)\n\n"
               "Now decide.\nA: {a}\nB: {b}\n\nAnswer with one word: SAME or DIFFERENT")

P_ATTACK = ("=== A CLAIM ===\n{c}\n\n=== YOUR ASSIGNED ANGLE ===\nAttack it on {a}.\n\nFind "
            "the ONE most damaging concrete failure on that angle. Name the situation where "
            "it goes wrong and what someone then wrongly concludes. Do not be balanced, do "
            "not summarise, do not switch angles.\n\nEnd with exactly one line:\n"
            "KILL: <one sentence>")

# REVISED MUST CARRY THE WHOLE PROPOSAL, NOT A SENTENCE.
# The one-sentence constraint came from critique.py, where every target genuinely WAS a
# one-sentence procedure. Applied to a multi-part proposal it is destructive: the first
# landed attack replaced the entire idea with a single qualifying clause, every later round
# attacked that clause, and after six attacks the output was a narrow edge case with the
# original proposal gone — one output still referenced a component no longer present in it.
#
# It also corrupts the measurement. A whittled-down fragment is EASY to defend, having less
# surface, so held/faced was partly rewarding narrowness rather than quality.
P_DEFEND = ("=== YOUR CLAIM ===\n{c}\n\n=== AN ATTACK ===\n{atk}\n\nAnswer it. Defend "
            "unchanged, or change the claim — but if you change it say exactly what changed "
            "and why the attack forced it. Do not concede vaguely.\n\n"
            "Then restate the claim IN FULL — not a summary, not the amendment by itself, "
            "but the complete proposal as it now stands including every part the attack did "
            "not touch, so that it stands alone without the original.\n\n"
            "End with exactly two lines:\nOUTCOME: HELD or MOVED or BROKE\n"
            "REVISED: <the complete claim as it now stands>")

P_NEWANGLE = ("=== A CLAIM ===\n{c}\n\n=== ANGLES ALREADY USED AGAINST IT ===\n{used}\n\n"
              "Name ONE genuinely different angle of attack — a kind of failure none of the "
              "above would catch. If every remaining angle is a restatement of one already "
              "used, say NONE.\n\nOne line:\nANGLE: <short name> - <what it examines>")

P_FALSIFY = ("=== A CLAIM ===\n{c}\n\nName the single observation that would drop your "
             "confidence in this by more than twenty points. It must be something someone "
             "could actually observe or measure, not a change of opinion.\n\n"
             "One line:\nFALSIFIER: <the observation>")

P_COND = ("=== A CLAIM ===\n{c}\n\nIs this claim's truth conditional on some variable that "
          "has not been fixed? If so, name the variable and say what the claim becomes at "
          "each end of it. If it holds unconditionally, say NONE.\n\n"
          "Format EXACTLY:\nVAR: <the variable, or NONE>\nHIGH: <what is true when it is high>\n"
          "LOW: <what is true when it is low>")

BASE_ANGLES = {
 "MAGNITUDE":  "whether the effect it names is large enough to matter, or is real but minor",
 "TIMING":     "whether its timescale matches the timescale of what it is explaining",
 "COUNTER":    "the case where what it names is present but the effect does not appear",
 "SUFFICIENT": "whether it is the whole story or silently carries an unstated second mechanism",
 "PROXY":      "whether it explains the thing or explains something that merely tracks it",
}


# One global cap on in-flight requests. Without it, expressed parallelism (12 questions
# x 12 clustering workers) becomes 429s, and orlib's backoff converts the parallelism
# straight back into latency. With it, callers can express as much width as the shape of
# the work allows and the semaphore does the throttling in one place.
_GATE = __import__("threading").Semaphore(48)

class Terminal(RuntimeError):
    """A failure that retrying cannot fix — out of credit, bad key, model gone."""

# Errors that mean "stop the run", not "try again". A 403 key-limit is not a rate limit:
# orlib only backs off on 429, so a 403 fell straight through, ask() turned it into "",
# and the pipeline ran to completion on empty strings — producing a clean-looking results
# table with three identical rows. A billing failure became fabricated science. Never again:
# these abort the whole run loudly instead of degrading into plausible output.
_TERMINAL = ("limit exceeded", "insufficient", "quota", "invalid api key", "unauthorized",
             "402", "403", "no endpoints found")

def ask(p, temp=1.0, mt=2200, nr=False, tries=3, effort=None):
    last = None
    for _ in range(tries):
        with _GATE:
            r = call(M, [{"role": "user", "content": p}], max_tokens=mt, temperature=temp,
                     no_reasoning=nr, effort=effort)
        SPEND["calls"] += 1
        if r["ok"]:
            SPEND["in"] += r.get("inp") or 0
            SPEND["out"] += r.get("out") or 0
            if r["text"].strip():
                return r["text"]
            # ok but empty: reasoning ate the whole budget and content never started.
            # Raising max_tokens does not converge — a runaway trace eats 13750 as happily
            # as 2200 — so drop reasoning, which reliably frees the content channel.
            # NEVER recompute nr from mt: same()'s sub-calls already run with nr=True, and
            # a formula like (mt > 4000) discarded that and switched reasoning back ON for
            # exactly the calls that were failing. Escalation must be monotone.
            # Auto-think: first push effort up once (None -> high) before giving up on
            # reasoning, so a starved trace gets one smarter pass before we drop thinking.
            if nr is False and effort is None:
                effort = "high"
                last = f"empty content (finish={r.get('finish')}); raising effort"
                continue
            mt, nr = int(mt * 2.5), True
            last = f"empty content (finish={r.get('finish')})"
            continue
        last = str(r.get("err"))[:400]
        low = last.lower()
        if any(t in low for t in _TERMINAL):
            SPEND["fail"] = SPEND.get("fail", 0) + 1
            raise Terminal(last)
    SPEND["fail"] = SPEND.get("fail", 0) + 1
    # A silent "" is what let a billing outage masquerade as a measurement. If more than a
    # handful of calls die, the run is no longer measuring anything and must not continue.
    if SPEND.get("fail", 0) > 20:
        raise Terminal(f"{SPEND['fail']} failed calls; last: {last}")
    print(f"  [call failed after {tries}: {last}]", flush=True)
    return ""


def line(t, k):
    m = re.findall(rf"{k}\s*:\s*(.+)", t or "", re.I)
    return m[-1].strip() if m else ""


# Disk-backed. same() is now three calls per unique pair and is invoked O(n^2) by every
# clustering pass, so the memo is the most expensive object a run builds — and an
# in-process dict throws all of it away when the run is killed, which has now happened.
# Persisting it also means a re-run after a crash is nearly free on everything it already
# compared.
_SAMEMEMO, _SAMELOCK = {}, __import__("threading").Lock()
MEMO_PATH = os.path.join(OUT_DIR, "same_memo.jsonl")
if os.path.exists(MEMO_PATH):
    for _ln in open(MEMO_PATH):
        try:
            _r = json.loads(_ln)
            _SAMEMEMO[tuple(_r["k"])] = _r["v"]
        except Exception:
            pass

def same(a, b):
    """Memoised. draw_until_saturated re-clusters all accumulated texts each batch, so
    without this the pairwise judgements are recomputed from scratch every round —
    quadratic work redone linearly many times."""
    k = tuple(sorted((a.strip()[:300], b.strip()[:300])))
    with _SAMELOCK:
        if k in _SAMEMEMO:
            return _SAMEMEMO[k]

    def one(p, x, y):
        """None on a dead call — never False. A failed call that returns False reads as a
        confident DIFFERENT, gets memoised to disk, and becomes a permanent wrong verdict
        biasing every later run toward over-splitting. Silence is not a judgement."""
        raw = ask(p.format(a=x[:700], b=y[:700]), temp=0.0, mt=800, nr=True)
        if not (raw or "").strip():
            return None
        t = raw.upper()
        return "SAME" in t[:60] and "DIFFERENT" not in t[:60]

    # CORE OR PERM_SHOT+sym. No model returns the verdict; two judges contribute facts and
    # the combination is computed here. +sym asks both orderings and requires agreement,
    # which is a strictness knob (it can only turn SAME into DIFFERENT) and is why it pairs
    # with the permissive member rather than the strict one.
    core = one(P_SAME_CORE, a, b)
    if core:
        v = True                                  # OR short-circuits; no need for the rest
    else:
        s1, s2 = one(P_SAME_SHOT, a, b), one(P_SAME_SHOT, b, a)
        if core is None or s1 is None or s2 is None:
            # A verdict built on a dead call is not a measurement. Return the conservative
            # answer for this run and DO NOT poison the persistent memo with it.
            return bool(s1 and s2)
        v = bool(s1 and s2)
    with _SAMELOCK:
        _SAMEMEMO[k] = v
        with open(MEMO_PATH, "a") as fh:
            fh.write(json.dumps({"k": list(k), "v": v}) + "\n")
    return v


def complete_link(items):
    """Complete linkage: a cluster only forms when EVERY pair inside it is SAME.
    Transitive closure merged A with C through B and produced 100% agreement on every
    edge of the physiology run. This is the fix, and it is deliberately conservative —
    over-splitting costs a few calls, over-merging destroys the distinction that mattered."""
    n = len(items)
    if n < 2:
        return [[0]] if n else []
    pairs = list(itertools.combinations(range(n), 2))
    eq = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(same, items[i], items[j]): (i, j) for i, j in pairs}
        for f in as_completed(futs):
            eq[futs[f]] = f.result()
    def linked(i, j):
        return eq.get((min(i, j), max(i, j)), False)
    clusters = []
    for i in range(n):
        for c in clusters:
            if all(linked(i, j) for j in c):
                c.append(i); break
        else:
            clusters.append([i])
    return sorted(clusters, key=len, reverse=True)


def draw_until_saturated(make, rail=RAIL_DRAWS, batch=5):
    """Exhaustion, not a fixed N. Draw in batches; stop when a whole batch lands entirely
    inside clusters that already existed. An easy question saturates on batch two."""
    texts, clusters, rounds = [], [], 0
    while len(texts) < rail:
        with ThreadPoolExecutor(max_workers=batch) as ex:
            new = [f.result() for f in [ex.submit(make, len(texts) + i) for i in range(batch)]]
        new = [t for t in new if t]
        if not new:
            break
        before = len(clusters)
        texts += new
        clusters = complete_link(texts)
        rounds += 1
        if rounds > 1 and len(clusters) == before:
            break
    return texts, clusters


# ---------------------------------------------------------------- intake

def measure_trap(q):
    """The trap frame is the modal answer, and the mode is measurable rather than
    judgeable. Draw unscaffolded answers to saturation; the largest cluster is what a
    predator's search image would lock onto. No hand-written trap list, so this works on
    an arbitrary question — which is what the chat interface needs."""
    # mt must clear the reasoning budget. At 700 the reasoning consumed the whole
    # allowance on the harder questions and `content` came back empty, which produced
    # zero clusters and a silently absent mode.
    texts, clusters = draw_until_saturated(
        lambda i: ask(P_MODE.format(q=q, cond=""), temp=1.0, mt=2000))
    if not clusters:
        return None, [], []
    big = clusters[0]
    return texts[big[0]], [len(c) for c in clusters], texts


def build_chain(q, cond):
    raw = ask(P_CHAIN.format(q=q, cond=CONDITIONS[cond]), temp=0.9, mt=3000)
    return [s.strip() for s in re.findall(r"STEP\s*\d+\s*:\s*(.+)", raw)]


# ---------------------------------------------------------------- edge classification

def classify_edge(q, steps, k):
    """Two axes. web.py measured one and got 100% on all six edges."""
    prior = "\n  ".join(steps[:k + 1])
    conds = list(CONDITIONS)

    def one(i):
        c = conds[i % len(conds)]
        return line(ask(P_NEXT.format(q=q, prior=prior, cond=CONDITIONS[c])), "NEXT")

    texts, clusters = draw_until_saturated(one, rail=len(conds) * 2, batch=3)
    if not texts:
        return None
    agree = len(clusters[0]) / len(texts)
    consensus = texts[clusters[0][0]]
    on_chain = same(consensus, steps[k + 1])

    # ablation: does k+1 arrive without k? if so nothing was inferred at this edge.
    abl = line(ask(P_NEXT.format(q=q, prior="\n  ".join(steps[:k] or ["(nothing yet)"]),
                                 cond="")), "NEXT")
    load_bearing = not same(abl, steps[k + 1]) if abl else True

    # The 0.6 was a constant I picked, and thresholding a measured agreement destroys the
    # difference between 0.59 and 0.11. The label stays as a readable summary, but the
    # continuous value travels with it and `attention` — how much this edge deserves —
    # is graded rather than a bucket.
    if agree < 0.6:
        kind = "LEAP"
    elif not on_chain:
        kind = "DISPUTED"
    elif not load_bearing:
        kind = "NARRATION"
    else:
        kind = "FORCED"
    # low agreement OR the chain diverging from consensus both mean unresolved inference
    attention = round(max(1.0 - agree, 0.0 if on_chain else 0.75), 3)

    return {"k": k, "from": steps[k], "to": steps[k + 1], "kind": kind, "agree": agree,
            "attention": attention,
            "on_chain": on_chain, "load_bearing": load_bearing, "consensus": consensus,
            "alternatives": [texts[c[0]] for c in clusters], "ablated": abl}


# ---------------------------------------------------------------- hardening

def harden(claim):
    """Attack to exhaustion. Not five angles because five was a cap on scrutiny — run
    rounds until a whole round produces no displacement AND no new angle can be named."""
    cur, scars, angles = claim, [], dict(BASE_ANGLES)
    used, rounds = [], 0
    while rounds < RAIL_ROUNDS:
        todo = [a for a in angles if a not in used]
        if not todo:
            break

        def one(a):
            atk = ask(P_ATTACK.format(c=cur, a=angles[a]))
            rep = ask(P_DEFEND.format(c=cur, atk=atk[:4000]), temp=0.7)
            o = line(rep, "OUTCOME").upper().split()
            return {"angle": a, "kill": line(atk, "KILL"),
                    "outcome": o[0] if o else "?", "revised": line(rep, "REVISED")}

        with ThreadPoolExecutor(max_workers=6) as ex:
            got = [f.result() for f in [ex.submit(one, a) for a in todo]]
        scars += got
        used += todo
        rounds += 1

        moved = [g for g in got if g["outcome"] in ("MOVED", "BROKE") and g["revised"]]
        if moved:
            # Collapse guard: a "revision" much shorter than what it replaces is the model
            # handing back only its amendment. Losing the proposal is worse than carrying
            # an unrevised one, so a collapsing revision is rejected.
            cand = max((g["revised"] for g in moved), key=len)
            cur = cand if len(cand) >= 0.6 * len(cur) else cur
        else:
            # MEASURED: rounds=8 and 42 generated angles on a single run — the "no new
            # angle can be named" test never fires, because a model asked whether another
            # angle exists always says yes. Self-reported exhaustion does not terminate.
            # (Same lesson as obsess, which only stopped once its test became a string
            # comparison rather than a judgement.) Displacement is a FACT about outcomes:
            # a full round in which nothing moved means the attacks have stopped biting.
            break
        # can anything new even be asked of it?
        na = ask(P_NEWANGLE.format(c=cur, used="\n".join(f"- {a}: {angles[a]}" for a in used)),
                 temp=0.9, mt=500)
        spec = line(na, "ANGLE")
        if not spec or spec.upper().startswith("NONE"):
            break
        name = re.split(r"[-–:]", spec, 1)[0].strip().upper()[:14] or f"X{rounds}"
        if name in angles:
            break
        angles[name] = spec.split("-", 1)[-1].strip() if "-" in spec else spec

    held = sum(1 for s in scars if s["outcome"] == "HELD")
    return {"claim": cur, "original": claim, "held": held, "faced": len(scars),
            "scars": scars, "rounds": rounds}


def annotate(claim):
    """Falsifier and the conditional-on edge. 'It depends on X' is not a hedge — it is a
    typed edge asserting this claim's truth is a function of X. A linear pipeline has
    nowhere to put it, so it gets flattened into a hedge and discarded."""
    with ThreadPoolExecutor(max_workers=2) as ex:
        f = ex.submit(ask, P_FALSIFY.format(c=claim), 0.7, 700)
        c = ex.submit(ask, P_COND.format(c=claim), 0.7, 900)
        ft, ct = f.result(), c.result()
    var = line(ct, "VAR")
    cond = None if (not var or var.upper().startswith("NONE")) else {
        "var": var, "high": line(ct, "HIGH"), "low": line(ct, "LOW")}
    return line(ft, "FALSIFIER"), cond


# ---------------------------------------------------------------- store

def nid(claim):
    return hashlib.sha1(claim.strip().lower().encode()).hexdigest()[:12]


class Graph:
    def __init__(self, path=STORE):
        self.path, self.nodes, self.edges, self.merges = path, {}, [], []
        if os.path.exists(path):
            for ln in open(path):
                try:
                    r = json.loads(ln)
                except Exception:
                    continue
                if r.get("_") == "n":
                    self.nodes[r["id"]] = r
                elif r.get("_") == "e":
                    self.edges.append(r)
                elif r.get("_") == "m":
                    self.merges.append(r)

    def _w(self, rec):
        with open(self.path, "a") as fh:
            fh.write(json.dumps(rec) + "\n")

    def add_node(self, claim, **kw):
        i = nid(claim)
        if i in self.nodes:
            return i
        r = {"_": "n", "id": i, "claim": claim, "t": time.time(), **kw}
        self.nodes[i] = r
        self._w(r)
        return i

    def add_edge(self, src, dst, typ, span="", strength=None):
        r = {"_": "e", "src": src, "dst": dst, "type": typ, "span": span,
             "strength": strength, "t": time.time()}
        self.edges.append(r)
        self._w(r)

    def articulation(self):
        """A node whose removal disconnects a large subgraph is an unexamined load-bearing
        assumption. This is one of the three graph events that ARE insight, structurally —
        you query for it instead of hoping a model emits it."""
        adj = {}
        for e in self.edges:
            if e["type"] in ("supports", "entails", "presupposes", "conditional-on"):
                adj.setdefault(e["src"], set()).add(e["dst"])
                adj.setdefault(e["dst"], set()).add(e["src"])
        if not adj:
            return []
        def comps(skip):
            seen, n = set(), 0
            for s in adj:
                if s == skip or s in seen:
                    continue
                n += 1
                st = [s]
                while st:
                    v = st.pop()
                    if v in seen or v == skip:
                        continue
                    seen.add(v)
                    st += list(adj.get(v, ()))
            return n
        base = comps(None)
        return [v for v in adj if comps(v) > base]

    def support_cycles(self):
        """A cycle in the support edges is circular evidence that reads as independent
        confirmation. Cheapest real error-detector in the whole design."""
        adj = {}
        for e in self.edges:
            if e["type"] in ("supports", "entails"):
                adj.setdefault(e["src"], []).append(e["dst"])
        out, state = [], {}
        def dfs(v, path):
            state[v] = 1
            for w in adj.get(v, []):
                if state.get(w) == 1:
                    out.append(path[path.index(w):] + [w] if w in path else [v, w])
                elif not state.get(w):
                    dfs(w, path + [w])
            state[v] = 2
        for v in list(adj):
            if not state.get(v):
                dfs(v, [v])
        return out


# ---------------------------------------------------------------- the loop

def run(q):
    t0 = time.time()
    g = Graph()
    print(f"graph: {len(g.nodes)} nodes, {len(g.edges)} edges carried in\n", flush=True)

    print("measuring the mode (this is the trap frame — not written, drawn)...", flush=True)
    trap, sizes, _ = measure_trap(q)
    print(f"  clusters {sizes}   mode: {(trap or '')[:150]}\n", flush=True)
    qid = g.add_node(q, kind="question")
    tid = g.add_node(trap or "(no mode found)", kind="trap")
    g.add_edge(tid, qid, "conditional-on", span="measured mode of unscaffolded draws")

    print("building chains under decorrelating conditions...", flush=True)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {c: ex.submit(build_chain, q, c) for c in ("plain", "foreign", "defeat")}
        chains = {c: f.result() for c, f in futs.items()}
    for c, s in chains.items():
        print(f"  {c:<8} {len(s)} steps", flush=True)

    steps = max(chains.values(), key=len)
    if len(steps) < 3:
        print("chain failed to parse"); return

    print(f"\nclassifying {len(steps)-1} edges (draws run to saturation, not to a count)...\n",
          flush=True)
    edges = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(classify_edge, q, steps, k) for k in range(len(steps) - 1)]
        for f in as_completed(futs):
            e = f.result()
            if not e:
                continue
            edges.append(e)
            print(f"  edge {e['k']}->{e['k']+1}  {e['kind']:<9} agree {e['agree']:.0%}  "
                  f"{len(e['alternatives'])} distinct", flush=True)
    edges.sort(key=lambda e: e["k"])

    prev = None
    for e in edges:
        i = g.add_node(e["to"], kind="step", entailment=e["agree"], edge_kind=e["kind"])
        if prev:
            g.add_edge(prev, i, "entails" if e["kind"] == "FORCED" else "supports",
                       span=e["from"][:200], strength=e["agree"])
        prev = i
        for alt in e["alternatives"][1:]:
            a = g.add_node(alt, kind="alternative", entailment=None)
            g.add_edge(a, i, "contradicts", span=e["from"][:200])

    spend = [e for e in edges if e["kind"] in ("LEAP", "DISPUTED")]
    print(f"\nspending on {len(spend)} of {len(edges)} edges "
          f"({[e['kind'] for e in spend] or 'none'}); the rest are forced or narration.\n",
          flush=True)

    hardened = []
    for e in spend:
        cands = e["alternatives"][:3] + ([e["to"]] if e["kind"] == "DISPUTED" else [])
        with ThreadPoolExecutor(max_workers=3) as ex:
            hs = [f.result() for f in [ex.submit(harden, c) for c in cands]]
        for h in hs:
            fal, cond = annotate(h["claim"])
            h.update(edge=e["k"], falsifier=fal, conditional=cond)
            i = g.add_node(h["claim"], kind="hardened", robustness=h["held"] / max(1, h["faced"]),
                           held=h["held"], faced=h["faced"], falsifier=fal,
                           scars=[{"a": s["angle"], "o": s["outcome"], "k": s["kill"]}
                                  for s in h["scars"]])
            if cond:
                c = g.add_node(cond["var"], kind="variable")
                g.add_edge(i, c, "conditional-on", span=f"{cond['high']} | {cond['low']}")
            hardened.append(h)

    hardened.sort(key=lambda h: (-h["held"] / max(1, h["faced"]), -h["faced"]))

    print("=" * 80)
    print(f"{'held/faced':>11}  {'rounds':>6}   claim")
    for h in hardened:
        print(f"{h['held']:>5}/{h['faced']:<5}  {h['rounds']:>6}   {h['claim'][:88]}")
        if h["falsifier"]:
            print(f"                        falsified by: {h['falsifier'][:80]}")
        if h["conditional"]:
            print(f"                        depends on:   {h['conditional']['var'][:80]}")
        for s in h["scars"]:
            if s["outcome"] in ("MOVED", "BROKE"):
                print(f"                        - {s['angle']} {s['outcome']}: {s['kill'][:70]}")

    art, cyc = g.articulation(), g.support_cycles()
    print(f"\nload-bearing assumptions (removal disconnects the graph): {len(art)}")
    for a in art[:6]:
        print(f"  {g.nodes[a]['claim'][:96]}")
    print(f"circular support (evidence that looks independent and is not): {len(cyc)}")
    for c in cyc[:4]:
        print("  " + " -> ".join(g.nodes[x]["claim"][:38] for x in c))

    cost = SPEND["in"] * 0.14 / 1e6 + SPEND["out"] * 0.28 / 1e6
    print(f"\ngraph now {len(g.nodes)} nodes / {len(g.edges)} edges -> {STORE}")
    print(f"[{time.time()-t0:.0f}s  {SPEND['calls']} calls  ${cost:.4f}]")


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or (
        "A patient with severe COPD and chronic CO2 retention is given supplemental oxygen. "
        "Their arterial CO2 rises. Explain the mechanism — what actually causes it to go up?")
    run(q)
