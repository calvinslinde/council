# Conditions, regimens, and arrangements

**Vocabulary.** A *condition* is a state the worker is in — damage, defeat, play, no
self-monitoring, blindness to the search image. Static; it wraps whatever else is happening.
A *regimen* is a process it runs — sleep, obsession, travel, rehearsal, amplification. It has
stages and duration. A *selector* chooses what continues — singleton, compression, generative
yield, frequency-dependence. Conditions were run as experimental arms for most of a session
before this carve existed; they are not arms, they wrap.

---

## The stage table

**Sixty-four runs** — 4 goals × 16 pipelines, the whole rebuilt library, validated judge.
Supersedes the 32-run table; where they disagree, this one is right.

| stage | free | trapped | ratio |
|---|---|---|---|
| crossattack | 19 | 5 | **3.8** |
| consolidate | 22 | 6 | **3.7** |
| harvest | 9 | 3 | 3.0 |
| peakshift | 3 | 1 | 3.0 |
| gen_many | 28 | 16 | 1.8 |
| compress | 5 | 3 | 1.7 |
| gen | 12 | 8 | 1.5 |
| rehearse | 7 | 5 | 1.4 |
| apostatic | 8 | 8 | 1.0 |
| worked | 10 | 10 | 1.0 |
| obsess | 5 | 7 | **0.7** |

### THE LIBRARY DOES NOT COMPOUND

Plain `gen`, one call, no scaffolding: **3 of 4 free (75%)**. The whole library averaged over all
64 runs: **42/64 (66%)**. *The average arrangement is worse than a single unscaffolded call.*

Three pipelines were free on all four goals, and **every one of them contains `crossattack` and
`consolidate`. No exceptions.**

    crossattack -> harvest -> consolidate
    gen_many(play) -> consolidate -> crossattack
    crossattack -> gen_many(play) -> consolidate

### WHY THOSE TWO

The variable that predicts a stage's ratio is not what human phenomenon it models. It is
**whether its gradient needs ground truth.** An attack lands or it does not; a compression ratio
is a fact about the text. Both check themselves.

Everything at or below 1.4 is a **posture** — a prompt asking the model to be in a state.
Postures are free to write and they do not survive measurement. *Postures don't survive;
instruments do.* This is the same finding as "evaluation is the bottleneck", arriving from the
other end: it is not only that my judges were broken, it is that generators must carry their own.

### RETRACTIONS FORCED BY THIS RUN

- **`worked` is 1.0, not 5.0.** The 10/2 came from n=12; at n=20 it is 10/10. "The strongest
  single validation of any rebuild" was noise. Withdrawn.
- **`obsess` is 0.7** — below one, i.e. actively harmful as a chain stage. The independent
  rebuild agrees: `obsess2d` circled and self-halted in 4 passes on a verbatim repeat. Keep it as
  a standalone deep-dive; remove it from arrangements.
- **`apostatic` is 1.0, and this is a bad test, not a bad condition.** It maintains polymorphism
  across a *population*; a linear chain has no population for it to act on.
- **DIAGNOSIS flipped from hardest (5/8) to easiest (14/16).** The earlier ranking was an
  artifact of which 8 pipelines it happened to draw. Do not trust per-goal difficulty at n=8.

**Also superseded:** stretch is not 4/0 (3/1 in-search, 1/3 alone — it was inheriting an axis
from upstream). `gen_many → compress` is not "the most robust finding" — it is the most *used*
pair and among the weakest ratios. "Material before generation" as stated was wrong.

---

## THE GOAL DETERMINES THE ARRANGEMENT

The single most useful finding. Goals split into two families and the pipelines split with them.

**Convergent goals** — a hidden truth exists (mechanism design, causal diagnosis).
**Open goals** — no right answer (design, premise).

| pipeline | convergent | open |
|---|---|---|
| `worked → gen_many(play) → compress` | **free** | trapped |
| `gen_many(play) → compress → gen_many(play) → compress` | trapped | **free** |

Exact complements. **If there is a truth to find, import a solved analogue. If there is not,
generate wide and compress repeatedly.** "Which pipeline is best" was the wrong question.

**Free on all four goals:** `worked → harvest → compress` and `gen → worked → stretch`.
DIAGNOSIS was hardest at 5/8 — causal problems with a hidden answer resist these most.

---

## JUDGE — the instrument, and why nothing older is trustworthy

Three evaluator failures in one session, all noticed only after building on the result: a
bisociation gate that presupposed its own conclusion; a novelty checker fooled into calling a
known mechanism new because it was described in counterpoint vocabulary; a trap checker that
scored three logging procedures FREE against a trap list containing "a practice log".

All three asked a **categorisation judgement** — *is the central move one of these?* — which
has room to be argued around, and the model argues around it.

**The fix: decompose into atomic questions about what the answer LITERALLY REQUIRES, ask each
independently, combine in Python. No model ever returns a verdict.**

Validated on twenty hand-labelled cases written before running. The combination rule was
**derived from the data, not from my theory of the trap**: my hand-written five-term rule with
an exemption clause got 85%; searching all simple rules over the collected fact vectors gives

```
trapped = writes | rates | counts        19/20 = 95%
```

The two terms I was most confident about had to go. **17 of 42 previously-scored outputs
flipped** when re-measured.

**Stated limit:** it detects the record-and-compare family cleanly and cannot distinguish a
helpful observer from a judging one.

---

## Arrangements

### WORKED-ANALOGUE — the strongest single condition
`extract structure (nouns stripped) → find a SOLVED problem in a distant field with that
structure → hand over the worked solution in its own vocabulary → generate`

**Structurally near, superficially far** — the worked-example condition. Structure gives
transfer; surface difference prevents copying. The structure statement is deliberately NOT
passed to the generator, so it cannot shortcut to the analogy.

Produced the Bruceton up-and-down staircase (from explosives sensitivity testing) for an
unmeasurable-progress problem. **Status: 10/2, best stage.** Cost: ~10x the latency of a plain
call, three sequential steps.

### CROSS-ATTACK — the refutation engine
`generate(damage) → attack from ASSIGNED angles → reply → record DISPLACEMENT → no synthesis`

**The only mechanism where evaluation is internal, adversarial and needs no ground truth.** An
attack either lands or it does not and the attacked party can answer — nobody needs to know
the right answer for the process to have a gradient. That is why it is the one thing that has
worked from the beginning.

**Measure displacement, not survival.** An attack that changes nothing was decorative. Three
outcomes: HELD, MOVED, BROKE.

Run on this project's four best procedures: **80–100% displacement, 17 of 20 attacks forced a
change.** It found that the clay procedure is *physically invalid* — clay shrinks as it dries,
so comparing a month-old dried impression to a fresh wet one measures the clay, not the hand.
I had called that the best artifact of the session twice.

Angles must be **assigned**, so an attacker cannot pick the one it can most easily win.

### SLEEP — consolidation, not pruning
`encode many, salience-tagged → global downscale → replay the tagged subset under a bounded
budget → NREM gist → REM integrate against the standing ledger → answer BEFORE reasoning →
justify separately, may not revise`

Consolidation is **training a slow statistical learner on replayed samples from a fast episodic
buffer**. What transfers is the regularity; the episode is discarded by design — which is why
the answer is small and why you cannot reconstruct the derivation.

**Two fixes were needed and both came from noticing a conflation, not from new research.**
Integration must *discard*, not accumulate — v1 grew longer every cycle and regressed in
generality 16 times out of 18. And **short is not the same as abstract**: compressing to a
proposition produced a 1–10 rating scale, because a proposition about gaps can only
instantiate as measuring gaps. The schema must stay **short and concrete**, keeping one thing
you could point at.

With both: *press your palm into wet clay at sunrise, date it, press another next month, run
your fingers over the two.* (Then broken by CROSS-ATTACK. Both facts belong here.)

**Cycle depth, re-measured after the fix: 2/18 climbed in abstraction, 18/18 said something
new** — and schema length rose 115 → 190 chars across seven cycles *despite an explicit
must-be-shorter constraint*. The transition matrix is zero at every step from cycle 3 on.
So: **sleep is a novelty generator, not an abstraction ladder**, more cycles buy new content
and no generality, and the discard instruction is not being obeyed. Unfixed, and the honest
statement is that prompting alone has now failed twice to make integration subtractive.

### OBSESS — wanting, not liking
`derive → NEARLY / MISSING / NEXT → compress the notebook (conclusions kept, reasoning
destroyed) → the object supplies the next question → off-task pass every third → stop when it
circles`

Dopamine mediates **wanting**, not pleasure, and ramps at **maximal uncertainty** — near p=0.5,
not at certainty. v1's every pass succeeded, which is the condition under which seeking shuts
off. Perseveration repeats something *certain*; obsession returns to something *uncertain and
nearly reachable*. The difference is prediction error, and when it hits zero the pull ends.

**Forgetting is the engine.** You cannot retrieve your own earlier reasoning, so you rebuild
it, and the rebuild differs, and the difference is the progress. Confirmed from three
independent directions. I nearly replaced the compressed notebook with append-only notes,
which would have removed the mechanism.

**The stopping condition took four attempts** and the working one is a string comparison. Two
semantic detectors missed three pairs of *verbatim-repeated* questions sitting in the output.

### REHEARSE — a forward model, not a generator
`fix the world externally → inhabit it in internal kinesthetic register → account for the
intervals → report SURPRISE, not failure → discard the run if nothing surprised it`

Motor imagery is the **forward model run offline**. It is documented for rehearsing an action
you already have; used as a generator it produces movies. **A simulation surprises you; a movie
confirms you.** Failures are cheap to confabulate; surprise is not.

The fatal flaw in v1: the simulator was **authoring the world it simulated in**, so nothing
could resist it. The world is now enumerated in a separate call and is immutable.

Found that shredding a written question *"doesn't make it go away — it just makes a sound"*,
which produced the raw-versus-polished divergence procedure.

### APOSTATIC — frequency-dependence as perception, not preference
`cluster → the largest cluster becomes a SEARCH IMAGE the evaluator cannot perceive → consume
the common morph → survivors reproduce with variation`

Predators form a search image for the common morph and take it; rare morphs survive **because
they are not detected**. The old version computed `1/(1+cluster_size)` as a priority — a
preference, which is not the mechanism at all. And it had **no heredity**, so it was a
scheduler, not selection.

Six rounds: after the first, **no cluster ever exceeded one member.** Eight workers, eight
modes, sustained. Never fixates — which is the property that "scaling forever" requires.

*I also measured the wrong thing originally:* apostatic selection does not predict rising
diversity, it predicts maintained polymorphism. I tested for mode count, got noise, and filed
it unproven.

### PEAK SHIFT — amplification, directional and bounded
`name the axis on which it departs from the typical → amplify ALONG THAT AXIS ONLY → stop when
it no longer solves the original problem, take the step before`

A gull chick pecks harder at an exaggerated beak than a real one; caricatures are recognised
faster than photographs. **The trap frame is the mean**, so displacement along the distinctive
axis is displacement out of the trap by construction.

*Not darker — bigger.* Darker escalates valence, which is cheap. Bigger escalates the
magnitude of the distinguishing feature.

Directional-iterative 3/3 free; undirected one-shot **0/3** — it either falls back into the
mean or blows past coherence. Usable range is one to two steps.

### EXILE — travel with no phrasebook and no return ticket
`translate the problem into a foreign system → solve there, never having seen the original →
a third worker brings it home, not knowing what was asked`

Adaptation mediates the whole effect of living abroad; exposure does nothing. The tame version
failed 6/6 because **the worker travelled and the problem stayed home** — the foreign system
sat beside an intact home frame as decoration.

Forced version: 3 of 4 free against a trapped control.

---

## Forbidden

- **Sleep on harvested singletons** — the support threshold destroys the material worth having.
- **Frequency-dependent selection inside obsession** — it penalises returning, which is the
  operation.
- **Anosognosia with rehearsal in one worker** — they are the same system at two ends (one runs
  the forward model, the other disables the comparator that checks it). Incoherent together,
  strongest pair in sequence.
- **Any semantic judgement inside a generation loop.** A regex is a fact about the text, not an
  evaluation, and may stay.
- **More than two removals per worker** — lose one function and the system reorganises around
  it; lose four and you do not get a savant, you get a patient.
- **Undirected collision** — tested and dead. 1/4 against directed 2/4. It was a superstition.

---

## THE GRAPH DOES NOT EARN ITS KEEP — settled by measurement

Three arms, 5 hard questions, blind scoring on 4 **held-out** attack angles no arm saw
while generating. Judge validated first (see SAME below); this is the first A/B run on a
working instrument.

| arm | what it is | escaped | robust ≥75% | mean held/faced |
|---|---|---|---|---|
| A_gen | one plain call | 0/5 | 0/5 | 0.35 |
| **B_ops** | **generate, then attack to exhaustion** | 4/5 | **4/5** | **0.70** |
| C_graph | measured trap → chains → edge classification → harden | 5/5 | 1/5 | 0.40 |

**B beats the baseline on 5 of 5 questions** (unanimous; sign test p=0.03 even at n=5).
**B beats the graph on 4 of 5.** The graph is indistinguishable from a single plain call
— 1 win, 1 loss, 3 ties.

**Why the graph loses to the same operators run without it.** Both arms use identical
`harden`. The difference is *what gets hardened*: C hardens candidates pulled off
LEAP/DISPUTED edges — **mid-chain fragments** — while B hardens a complete answer. A
fragment is a worse object to attack: narrower, partial, missing the context that makes it
defensible. C escaped the mode 5/5 and held only 1/5, which is exactly the contrarianism
cell the two-axis design exists to detect.

**Caveats, neither of which rescues it.** ESCAPED is unfair to A by construction (the mode
is measured from plain draws, so a plain draw cannot escape it) — the robustness column is
the fair comparison and says the same thing. And these 5 are mechanism/diagnosis questions;
design and conceptual ones are where a graph would have its best remaining case.

**The insight-query story is mostly dead too.** Support cycles fired `[0,0,0,0,0]` — never,
once. Articulation points fired 11–13 per graph, but on a near-path graph every interior
node is an articulation point, so that detects "this is a chain", not insight.

**What survived: the substrate is `harden`.** Generate, attack to exhaustion from assigned
angles, keep the revision. No decomposition, no chains, no graph.

## VOID RUNS — recorded so nothing downstream cites them

- **`web.py`** (claim graph, blind re-derivation): all six edges scored 100% agreement. Cause:
  transitive-closure clustering plus a permissive `same()` merged everything. Zero resolution.
- **`ab.py`** (three-arm A/B, 15 questions): every arm escaped 11/11, held 0/11, every edge
  classified LEAP. Cause: **the OpenRouter key hit its monthly cap mid-run.** `orlib` only backs
  off on 429, so the 403 fell through, `ask()` returned `""`, and the pipeline ran to completion
  on empty strings — `same()` returns False on empty, so nothing clustered, nothing matched the
  mode, and the scorer parsed nothing. One dead call cascaded into five degenerate metrics.

**A new failure class, and the worst one yet: it did not crash, it produced science.** Three
identical rows and a clean table. The three broken judges at least produced *wrong* numbers;
this produced *fabricated* ones. `ask()` now raises `Terminal` on 403/quota/bad-key and aborts
past 20 dead calls; empty-but-OK responses escalate `max_tokens` rather than being accepted.

## SAME() — the unvalidated instrument under everything

`same()` decides clustering, mode measurement, edge classification and ablation. It was
validated on **zero** cases while `judge.py` sat two files away as the record of why that is
fatal. Tuned twice by hand and overshot in both directions — permissive merged everything,
strict merged nothing. Both runs void.

`samejudge.py` now holds **44 pairs from real re-derivations, hand-labelled before any variant
was written**, searching 4 prompts × 2 symmetry modes. It scores over-merge and over-split
separately on purpose: **over-merging destroys a distinction permanently, over-splitting only
costs calls.** Blocked on the key.

## The standing lesson

Every failure this session was in the **instrument**, not the generator: three broken judges, a
filter that encoded its own conclusion, a saturated problem chosen because it had a baseline
rather than headroom, a logger printing `1` when it meant `0`, a join on truncated strings, a
fourth judge built without validation, and an API error that silently became a results table.

Generation is infinite and costs nothing. **Evaluation is the entire bottleneck**, and the only
evaluators that scale are the ones needing no ground truth: counts, adversarial survival,
compression ratio, and fact-decomposition combined in code.

And the corollary the void runs added: **an instrument must fail loudly or it will fabricate.**
Silence is indistinguishable from a measurement.
