# Cheap-swarm creativity — findings

> **READ COMBOS.md FIRST.** It carries the current state. This file is the historical record
> of how it was arrived at, and several of its headline claims were later overturned — kept
> deliberately, because a record that quietly deletes its own errors is not a record.
>
> **Superseded by later measurement:**
> - *"Material before generation is the most robust finding"* — WRONG as stated. `material`
>   was the worst stage in the library (1 free / 3 trapped). Rebuilt as **worked examples**
>   (structurally near, superficially far) it became the best (10/2). Material about the
>   problem is worse than no material at all.
> - *"stretch is 4/0, the strongest stage"* — it is 3/1 in-pipeline and **0/3 standing alone**.
>   It was inheriting a direction from upstream stages. It needs a named axis.
> - *"gen_many → compress is the most robust finding"* — the most *used* pair, and the two
>   weakest ratios in the table.
> - *"Sleep is a failure"* — it is a depth mechanism fed undiversified input. It later produced
>   the best procedure in the project.
> - *"Co-presence is the only operation that survives"* — an artifact of a circular filter.
> - *"Some deficits are simply unreachable"* — asserted on n=1; it succeeded next run.
> - **Every number produced before `judge.py` was validated is untrustworthy.** 17 of 42
>   re-scored verdicts flipped.
>
> **Still standing:** cross-attack as the refutation engine · the 38:1 trace-to-answer ratio ·
> enforcement beats request · play buys spread and costs compliance · the goal determines the
> arrangement.

*Session 2026-08-03. DeepSeek v4 Flash 0731 only, via OpenRouter. Total spend well under $1.*

The question: can a council of very cheap models match or exceed a strong single model,
and specifically can it be made **creative** — not just more thorough.

---

## 1. What was measured, including the results that killed ideas

**Verifiable single-answer problems — councils have nothing to add.**
Across 220 samples / 18 items: pass@1 = 0.920, pass@10 = 1.000, majority = 1.000,
**headroom over majority-vote = 0.000.** Best-of-N plus a vote already saturates.
Diagnosis: brute-forceable gold answers means *canonical* problems, so the construction
method selected for exactly what the model is best at. Never found a problem class where
the model is confidently and consistently wrong — the one regime where attack beats vote.

**Head-to-head, open research problem** (error-decorrelation under three constraints),
Opus in-harness vs. the DeepSeek council:
- Council **won** on refutation — found a Bayes-error impossibility result Opus missed
  entirely, and landed a real hit on Opus's central mechanism.
- Opus **won** on construction — the quantitative identity, numerical self-verification,
  two actual proofs, implementability.
- Cost: **$0.023 vs ~$1.60, ~70x.**
- Conclusion: **cheap-and-many is a refutation engine, not a construction engine** — and
  the value concentrated entirely in the forced-lens attacks.
- Caveat that still stands: n=1, and I was the judge.

**Four grader bugs, each of which had produced a false capability reading.** Angle brackets
from my own template, unstripped `<answer>` tags, bare `sqrt2`, and a unicode `√` replaced
*after* the sqrt regex ran. `grade.py` was rewritten with 18 unit tests. Every headline
number before that was false. This is the single most important operational lesson: an
unverified harness manufactures capability that isn't there.

---

## 2. The theory that survived

**Costume vs. travel.** Role prompts and "mandated lenses" re-weight vocabulary, not
trajectory. Measured: four lenses produced four vocabularies for one idea. Loading actual
foreign *material* displaces the distribution; asking for a perspective does not.

**Where the creative act happens.** One low-probability choice very early, then entirely
ordinary execution. In all three trap problems the whole answer is fixed by a single noun
phrase — the measured quantity, what stands in for a label, what differs between systems.
Consequence: raising temperature globally is precisely wrong. You want maximum entropy at
the branch point and zero everywhere else.

**Why one model can't.** The plausibility filter runs *during* generation, so low-prior
candidates are suppressed before they're written. The knowledge is present; the emission
is not. Recall and evaluation running simultaneously is the whole failure.

**Undirected expansion beats directed search.** Never ask how to connect X to the problem —
the question's own vocabulary re-imports the frame. Ask what X does, exhaustively, with the
problem absent from the prompt, and the connection falls out of the expansion.
*Demonstrated on myself:* asking "how do mouse and human trials differ" with all biology
stripped out surfaced **housing temperature** — lab mice live below thermoneutrality and are
chronically cold-stressed — a mechanism absent from my own full-effort sealed answer written
thirty minutes earlier.

**Assumption diff.** The relaxable assumption is never the one you were given, it's the one
you imported while reading. Enumerate the assumptions your attempt relies on, then check
each for literal presence in the problem text. Anything absent is free. Mechanical, not vibes.

---

## 3. The correction that reframed everything (Calvin's)

I spent most of the session trying to **free** the model from its prior. The historical
record says the opposite: you don't free people into creativity, you **trap** them into it.

Dostoevsky/Siberia, Beethoven/deafness, Milton/blindness-and-defeat, Ramanujan/isolation from
standard training, Darwin/five years at sea, Pascal/illness. **None of them chose it**, none
could escape it, and all had to keep going inside it. An artist who chooses to paint only in
blue is doing an exercise.

**And the mechanism is not absence — it's compensatory reorganisation.** Cross-modal
plasticity: Braille reading activates occipital cortex in blind readers, and TMS to that
"visual" area disrupts it, so it is load-bearing, not decorative. The machinery keeps running
on new input. The creativity is in the *repurposing*, and it needs use, pressure, and time.

Three design consequences:
1. **Enforce, don't request.** Every lens I wrote was a suggestion. *Confirmed empirically
   below:* asked politely, the model does not comply.
2. **Recruit, don't only prohibit.** Forbid a faculty as CONTENT while requiring its
   STRUCTURE to run on foreign material. V1 does Braille.
3. **Ablate the measured dominant mode**, not an arbitrary one. Cortex only reorganises when
   the dominant channel goes. Ban the *faculty*, not the *answer* — banning answers just
   walks to the next answer in the same modality.

**Where the plasticity lives.** The weights are frozen, so compensation has to accumulate in
the context. ACE already shows capability lives in context — so a persistent playbook *is*
the reorganised tissue. Not an analogy; the only available substrate.

---

## 4. Prior art — checked, not assumed

Most of what I derived independently is published. That the field converged on the same
structures is evidence the direction is right; it also means I should have searched first.

- **Capability lives in context — done and PROVEN.** ACE (arXiv 2510.04618): a smaller
  open-source model matches the top-ranked production agent on AppWorld overall and beats it
  on the harder test-challenge split. +10.6% agents, +8.6% finance. *Fetched and read.*
  Don't spend budget re-proving this.
- **Instruments that compound — a whole subfield.** Voyager (2023) onward. Metacognitive
  Reuse (2509.13237) is the "instruments are compressed context" claim exactly: recurring
  reasoning extracted from CoT, abstracted, **named**, invoked by name instead of
  regenerated. *Fetched and read.*
- **Abductive framing bypasses filters — confirmed from an odd direction.** The sharpest
  demonstration is jailbreak research (2509.10931): models treat inference tasks differently
  from direct queries. Same mechanism, different filter. Nobody appears to have pointed it at
  the *plausibility* prior for creative generation.
- **Constraint-as-creativity is Boden, ~1990.** Combinational / exploratory /
  **transformational** creativity; transformational = altering a dimension of the conceptual
  space so structures arise that couldn't before. That is the amputation argument, canonical
  and 35 years old.
- **Homogeneous debate underperforms.** "The Cost of Consensus" (2605.00914) — isolated
  self-correction beats unguided homogeneous multi-agent debate. Matches what I measured.
- **Convergence erodes evidence.** "The Deliberative Illusion" (2606.03032) — *factual
  attrition*: agents converge while the evidence base decays underneath them.
- **Novelty–utility tradeoff is documented.** Validity and success rate correlate negatively
  with novelty and diversity; as complexity rises, models fail by violating utility rather
  than by being unoriginal. Constraint's sign also **flips with task complexity** — helps on
  complex tasks, terminates exploration prematurely on simple ones.
- **NEGATIVE RESULT against the transplant idea.** MEMO (2603.09022): transferred context
  fills capability *gaps*, with the largest gains in the target's weakest areas — and
  **negative transfer where the target is already strong**, because source heuristics
  interfere. My plan was to harvest an impaired worker's technique and hand it to an
  unimpaired one, i.e. exactly the strong case.
  → **Design consequence:** the faculty isn't harvestable, it's *embodied*. The damaged
  worker stays in the council permanently as a member. Diversity comes from keeping damaged
  members, not from mining them.

*Provenance: ACE and Metacognitive Reuse were fetched and read. Everything else in this
section is search-snippet level and several are 2026 arXiv entries not vetted.*

---

## 5. The damaged council — first real result

`damaged.py`, six workers with permanent **harness-enforced** deficits on the `clock`
problem (determine time of day to one minute, arbitrary unknown location, heavily overcast,
no clock/oscillator/radio/prior sync). Regex enforcement where possible, fact-shaped LLM
compliance check otherwise. A violating output is voided with the violation quoted back and
the instruction that *the route it took is closed*. Novelty is the objective; validity is
recorded and **gates nothing** — nothing is killed on a depth-one evaluation.

**Enforcement is doing real work.** NO_NUMBER, NO_SKY and QUESTIONS_ONLY all violated on
their first attempt and were rejected. Direct evidence that the earlier "mandated lenses"
were decorative: asked politely, the model does not comply.

**Escapes, all absent from `opus_sealed.md`:**

| worker | mechanism |
|---|---|
| NO_PERIODIC | Extract the Sun's static gravitational tidal tensor; its principal eigenvector is the sundial. |
| NO_NUMBER | Solar and lunar tidal gradients reveal the Sun's line; local rotation axis gives hour angle. |
| NO_SKY | Measure the local direction of the charged-particle anisotropy; its rotation encodes time. |
| RECRUIT_BIO | Read the local biological community's circadian phase, averaged over many organisms. |

Why these count:
- **The gravitational sundial** is a genuinely different operation on physics my sealed file
  contains and dismissed. I had Earth tide and rejected it for lunar contamination — because
  I was reading the tidal *time series*. Reading the tensor's instantaneous *orientation*
  gives the Earth–Sun line, and gravity is not blocked by cloud. The deficit produced it:
  amputating phase-reading left a static field direction as the only route out.
- **Two independent amputations converged on it** — NO_PERIODIC and NO_NUMBER, from different
  deficits. Convergence from different damage is far stronger evidence than a single hit.
- **Cosmic-ray anisotropy** (NO_SKY): muon flux carries a solar diurnal anisotropy and
  penetrates overcast trivially. Not in the sealed file.
- **Population-averaged circadian phase** (RECRUIT_BIO): my sealed file dismissed biological
  markers in one line as too coarse. Averaging over N organisms with independent phase noise
  is the answer to my own objection, and I never made it because I'd closed the option.

Error budgets are not checked and one minute may not be reachable by any of them. That is
deliberately a later question.

---

## 6. Second wave — mechanisms from how minds actually work

`mind.py`, same problem, same scoring:
- **INCUBATE** — selective forgetting. Keep the abstract lesson, delete the specific failed
  route, return. Everything in the agent literature accumulates monotonically; this is the
  inverse, and forgetting on purpose is the point.
- **DREAM** — REM architecture. DLPFC down, associative cortex hot: dreams are narratively
  coherent and wildly implausible because the consistency checker stays on and the
  plausibility checker goes offline. Coherence enforced, plausibility explicitly suspended.
- **RECONSOL** — memory reconsolidation. Recall makes a memory labile and it re-stores
  altered. Lossy compress/expand cycles are structure-preserving mutation. Everyone else
  fights drift.
- **FORM** — the sonnet rather than the amputation. A rigid alien form whose *slots demand
  content*: differential diagnosis, legal contract, formal proof. Prose lets you skip; a slot
  makes omission visible.
- **SOMATIC** — Damasio. vmPFC patients have intact logic and cannot decide, because affect
  prunes the option space before justification. Ask what it would most *want* to be true.
- **LANG** — concepts carve differently across languages; reason in Chinese, recover the
  mechanism after, preserving distinctions English would blur.
- **PLAY** — declared in advance never to be evaluated. If the output changes, that is
  a direct measure of how much the evaluation was suppressing.

---

## 7. Operational lessons

- **`nohup`, and save incrementally.** A 23-minute run was lost to task teardown because the
  JSON dump was at the end. Both current runs write after every worker.
- **Reasoning models return empty `content` while spending the whole budget in `reasoning`.**
  Use very high `max_tokens` and retry on empty.
- `requests`, not `urllib` — urllib fails SSL cert verification on this Mac.
- Pin `deepseek-v4-flash-0731`. The bare alias is the older April build; `-latest` is a
  routing alias that will silently move.
- **The reasoning trace is being discarded on every call.** `orlib.call` captures it;
  nothing uses it. It contains the branches the model considered and rejected *before*
  emitting — exactly the suppressed candidates. Unmined.

## 8. Play, and why enforcement may be self-defeating

`damaged.py`'s PLAY-adjacent worker in `mind.py` was told nothing it wrote would be read,
scored, or compared to anything. **It produced the best answer in the entire run** -- the
Sun's cosmic-ray muon shadow, the most physically exact mechanism of thirteen. Removing the
evaluator did not lower its quality.

The literature explains it and indicts most of what I built:

- **Amabile 1979** -- expected evaluation reduces CREATIVE performance while leaving
  TECHNICAL MERIT unaltered. Expected evaluation is the single most deleterious extrinsic
  constraint, across the entire age span. So the trade is nearly free: what evaluation
  protects is not what it costs.
- **Amabile 1993** -- extrinsic motivation splits in two. INFORMATIONAL (feedback about what
  happened) is *synergistic* with intrinsic motivation. CONTROLLING (evaluation, deadlines,
  imposed constraint) undermines autonomy and disrupts engagement. Nearly everything built
  today is the controlling kind.
- **Vygotsky** -- "in play a child is always above his average age... a head taller than
  himself." Play produces ABOVE-ceiling performance, and the stretch is SELF-GENERATED with
  no adult directing it. An imposed constraint cannot create its own zone of proximal
  development.
- **The nuance that resolves the result:** play is NOT the absence of rules. It is voluntary
  submission to STRICT ones -- the child playing mother obeys the rules of motherhood more
  rigorously than a mother does. That is why the play worker was the most precise rather than
  the sloppiest. Under evaluation you select for DEFENSIBILITY, and defensibility tracks
  familiarity rather than truth. Rigour is not what we remove; consequence is.

**Convergent derivation:** DREAM (REM neuroscience: coherence on, plausibility off) and PLAY
(developmental psychology: strict rules inside a freely-adopted "as if") arrive at the same
structure from unrelated literatures. That is the strongest single piece of evidence in the
project for any mechanism.

`play.py` tests it: six identical restrictions, two arms, only the framing differs.
CONTROLLED keeps v1's imposed/rejected/"that output is void". PLAYED makes it voluntary
(chosen from a 3-menu), frames it as a world-fact with no evaluator implied and nothing to
work around, declares no-evaluation BEFORE generation (Amabile: it is the *expectation* that
damages), and gives informational feedback only. Early: **the PLAYED arm found a mode the
CONTROLLED arm did not** -- two workers independently reached solar neutrinos, which pass
through cloud, ground and the whole Earth. Nothing in any prior run reached it.

*v1 defect this fixes and names: v1 framed the rule as a fact ("a fact about you that cannot
be negotiated") and the retry as pure control ("that output is void"). Mixed, and untestable
as built.*

## 9. The reasoning trace -- 38:1

`damaged_raw.json` holds **378,685 characters of reasoning against 9,964 characters of
answer.** I discarded 97.4% of what every worker produced, on every call, all session, while
spending the session trying to manufacture exactly what was in it.

The trace records candidates the model CONSIDERED AND REJECTED before emitting anything --
the low-prior candidates the plausibility filter kills. **The tail was never deleted by
distillation. It was made unemittable, and it is sitting in a file.**

`harvest.py` mines it, splitting rejections two ways:
- **ARGUED** -- the trace cites a reason, a number, a physical constraint. A real constraint;
  goes to the negative ledger.
- **FELT** -- dropped for seeming exotic, impractical, far-fetched, or dropped with no reason
  at all. Pure filter, no argument. **Resurrect verbatim.**

Nothing is generated here. It is read back out, and it costs nothing because the data already
exists.

## 10. Neuroscience-grounded council (`neuro.py`)

Each worker is a documented intervention, not a metaphor:

- **ATL_SUPPRESS** -- Chi & Snyder: decrease left anterior temporal lobe excitability while
  increasing right ATL. **0/22 solved the nine-dot problem before; over 40% after ten
  minutes.** Same region whose degeneration in frontotemporal dementia produces acquired
  savant syndrome. Left ATL does SEMANTIC CATEGORISATION -- it files particulars into concept
  boxes, which is why acquired savants draw accurately from memory: they see the thing, not
  the category. **THE LABEL IS THE TRAP** -- "this is a timekeeping problem" retrieves
  timekeeping knowledge, and that retrieval happens before any reasoning does. So: ban
  categorisation itself; particulars and relations only.
- **REBUS** -- Carhart-Harris & Friston: psychedelics relax the PRECISION WEIGHTING of
  high-level priors, liberating bottom-up flow; therapeutically this relaxes "pathologically
  overweighted priors". The plausibility filter *is* an overweighted high-level prior. So:
  general knowledge is low-precision, this problem's particulars are high-precision, and
  where they conflict the particulars win.
- **LOW_LATENT_INHIBITION** -- Carson, Peterson & Higgins: reduced latent inhibition (failure
  to screen out stimuli tagged irrelevant) is associated with creative achievement. So:
  inject genuinely unrelated material and forbid ignoring it. The exact opposite of every
  prompt-engineering instinct.
- **FLAT_ASSOCIATIVE** -- Mednick: creative individuals have flat associative hierarchies,
  uncreative ones steep. So: the first three associates are unavailable.
- **HYPOFRONTALITY** -- Dietrich: flow involves transient prefrontal downregulation. So: no
  planning, no options, no meta-commentary, no revision. Forward motion only.
- **PARADOX_FACILITATION** -- Kapur: damage to one system RELEASES function in another it had
  been suppressing. So: name the faculty the problem most calls for, destroy exactly that,
  identify and use what it was suppressing.

## 11. The confabulating interpreter (`interpreter.py`)

- **Gazzaniga**: left hemisphere sees a chicken claw, right sees a snow scene, left hand
  picks a shovel. Asked why, the left hemisphere -- which never saw the snow -- says "you need
  a snow shovel to clean out the chicken shed." It did NOT say "I don't know", which was the
  true answer.
- **Johansson choice blindness**: subjects are handed the option they REJECTED; 75% never
  notice, and **87% readily volunteer detailed confident justifications for a choice they
  never made.** Two findings make it a mechanism rather than a curiosity: confabulation is
  strongest when internal evidence is WEAK (a gap-filler that fires where knowledge is thin),
  and afterwards **memory shifts toward the invented justification** -- the made-up reason
  becomes the belief.

**The model: confabulation inverts the direction of inference.** Normal reasoning fixes
premises and lets the conclusion float; the interpreter fixes the CONCLUSION and constructs
premises, and backward chaining searches a different region entirely. It generates rather
than hallucinates because the machinery must cohere with everything else known -- only the
conclusion is exempt. To justify the shovel the interpreter had to build a real causal story
about chicken sheds, and that story is false about the experiment and **true about the
world.**

=> **THE PRODUCT IS THE MACHINERY, NEVER THE CONCLUSION.** Every other worker generates
candidates; this one generates justification structure, which is why it can be pointed at any
output the others produce. And it is never given the option to doubt -- the left hemisphere
did not get to say "I don't know", and any prompt that permits hedging has destroyed the
experiment. The ABSURD arm (deliberately false conclusions) is the control: if the machinery
is still valuable when the conclusion is garbage, the conclusion really is irrelevant.

## 12. Still unexplored

Ranked, with the two largest first. Both were argued for at length and then not done.

1. **TOOLS.** A full turn was spent arguing that closed-book models never hit a REAL wall --
   they hit imagined walls and imagine their way past -- and that code execution is what makes
   re-representation forced rather than requested. Then six councils were built, all
   closed-book. Not one worker has executed anything or checked a number.
2. **The self-amputating ledger.** Six workers converged into tidal gravity together, so
   intuition-picked deficits run out. The ledger derives the next amputation from whatever the
   population converged on. The convergence data *demands* it; it is what makes this compound
   instead of plateau.
3. Harness-enforced non-concession with the forced translation as deliverable.
4. Define the slot, forbid the name -- operationally-defined slots with no retrievable label,
   aimed directly at the branch-point noun phrase.
5. The abductive ladder with a return trip (ascend filter-off, descend tool-verified; the
   residue is the finding).
6. Impossibility proofs as representation-locators.
7. Simulation residuals -- manufacture observations that exist nowhere.
8. Prompt-space search; the persistent notebook over hundreds of attempts; stakes and defeat;
   swarm-builds-the-test; attrition as feature extraction.

Neuro/psych mechanisms not yet touched: **semantic satiation** (cheapest possible left-ATL
suppression -- repeat a label until it dissolves), **split-brain proper** (two workers, no
channel, forced reconciliation through a narrow interface), **anosognosia** (a worker that
cannot perceive its own deficit -- every damaged worker so far knows it is damaged and reasons
around that knowledge), **Ganzfeld** (uniform structureless input reliably produces
hallucination -- the system manufactures structure when input carries none), **bisociation**
(Koestler), **structure mapping** (Gentner), **Poincare's aesthetic selection**, **the
prepared mind** for anomaly-noticing, and **synesthesia** as forced cross-modal binding.

## 13. Named combination checkpoints

Nine reusable pipelines are specified in `COMBOS.md`, each built on the principle that a
measured failure of one stage is caught by the function of the next:

  POSITION-THEN-DEPTH    position first then years — mechanics, exploit, singleton, obsess, sleep, immerse
  CROSS-ATTACK     the refutation engine — MEASURED, 70x cheaper than Opus, stop redesigning it
  TRACE-MINE       dig the refuse heap — 38:1 trace ratio, compression-selected, nearly free
  SINGLETON-DEPTH       minimal life arc — singleton, obsess, sleep
  DAMAGE-THEN-SLEEP      novelty then depth — damage into sleep, the pairing I mis-scored
  PAST-THEN-PRICE  walk past, then price — anosognosia into immersion, opposites in sequence
  RULE-EXPLOIT    know the rules, pick the lock — enumerate mechanics, then obey them somewhere
               nobody intended
  WANT-FIRST   for anything with a reader — wish + defeat, to break the elegy trap
  OBJECTION-CONSOLIDATE     consolidate the objections rather than the conclusions

Also in that file: the stage / modifier / selector vocabulary (most of this session was spent
running modifiers as if they were experimental arms — they wrap, they are not arms), and the
forbidden combinations.

## 14. Open threads

- Score both runs against `opus_sealed.md` and count tier-3 escapes properly.
- Harvest the reasoning traces. Free, plumbing exists, tests whether distillation deleted
  the tail or merely hid it behind the output filter.
- Run damaged workers across *many* problems so compensation actually accumulates — one shot
  gives a weirder worker, not a reorganised one. Plasticity needs duration and pressure.
- Tool-verified non-concession: agents holding code-backed proofs so concession is
  structurally impossible, with the forced translation as the deliverable. Closest thing to
  genuinely unclaimed ground found this session.
- Never measured: whether any of this beats Sonnet 5. A single 0731 call sits at AA index 50;
  Sonnet 5 is 53.
