# Council

A cheap-model swarm that attacks its own answer, and a judge that was checked against a person before its numbers were used.

Most of this repo is the thing that survived an August 2026 study of whether a group of very cheap models can stand in for one strong model. The study's record, including the claims that were later overturned, is in `FINDINGS.md`. The current state of the method is in `COMBOS.md`.

## What it does

`council.py` takes a question and runs the arm that won the comparison:

1. several cheap models answer from different starting conditions (not personas; different things they may assume or must avoid);
2. each answer is attacked from assigned angles until the attacks stop landing;
3. the revision that survives is kept.

The output ships with its scars, not with a self-assessment: the claim, how many assigned attacks it held, which attacks survived, what would falsify it, and what it depends on.

`judge.py` is the evaluator used to score answers. It was validated against hand-checked verdicts before it was trusted; 17 of its first 42 verdicts changed when that check was done, which is why it exists in this form.

`run_eval.py` runs the verifiable problem set in `eval_set.py` (short problems with one checkable answer, written as variants of classics so they are not memorised). `hard_set.py` holds the harder set.

## Requirements

- Python 3.10 or newer; `pip install -r requirements.txt` (only `requests`).
- An OpenRouter key in the `OPENROUTER_API_KEY` environment variable. On a Mac, a keychain item (service `openrouter`, account `key`) also works. The models named in `engine.py` are the free-tier ones that were available in August 2026; OpenRouter changes that list, so expect to edit the model names.

## Run it

```
python3 selftest.py                 # no network: imports, problem sets, output folder
python3 council.py "your question"  # prints the result; raw output goes to out/council_raw.json
python3 run_eval.py                 # the verifiable set
```

Raw outputs go to `out/` (or the folder named by `COUNCIL_OUT`); that folder is ignored by git.

## What it is not

- It is not a benchmark. The problem sets are small and were written for one study.
- The numbers in `FINDINGS.md` came from specific free models on specific days. They are a record, not a promise.
- On problems with one checkable answer, the group added nothing over a simple vote. The interesting result was on an open problem, in one trial, with one person judging. Read section 1 of the findings before quoting anything.

## Related

The answer matcher this study used, with its tests, is published separately as the [grader-check kit](https://github.com/calvinslinde/grader-check-kit).

## License

MIT. See `LICENSE`.
