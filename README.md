# How Much of MathQA Is Repetition?

Code for the paper *How Much of MathQA Is Repetition? A Copy Baseline With No Learned Weights Outperforms a RoBERTa Solver*.

No test question in MathQA is an exact copy of a training question, but most are training questions with only the numbers changed. This code measures that repetition and shows what a method that only copies from training can score.

## Quick start

Needs Python 3.9 or newer. The data downloads by itself the first time, and everything runs on a CPU in about a minute.

```bash
git clone https://github.com/Infiski/mathqa-audit
cd mathqa-audit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash run_all.sh
```

Results are printed and saved in `results/filtered.json` and `results/full.json`.

## Folder layout

```
mathqa-audit/
├── run_all.sh              runs the two scripts below
├── run_filtered.py         results on the filtered split
├── run_full.py             results on the full 37k dataset
├── src/
│   ├── utils.py            paths and data downloads
│   ├── interpreter.py      runs solution programs, one interpreter for each data format
│   ├── datasets.py         templates and answer checking for each version of the data
│   ├── baseline.py         the copy baseline (Rule 1 and Rule 2) and the no-shared-templates split
│   └── significance.py     exact McNemar test and paired bootstrap
├── deduct_reasoner/
│   ├── requirements.txt    packages for this step only
│   ├── run_checkpoint.py   runs the released DeductReasoner checkpoint
│   └── compare.py          compares DeductReasoner with the copy baseline
├── data/
│   ├── filtered/           16,191 / 2,411 / 1,605 problems (downloaded)
│   └── full/               29,837 / 4,475 / 2,985 problems (downloaded)
└── results/
```

## The copy baseline

The baseline has no learned weights. It uses only the training questions and their programs.

- **Rule 1 (lookup):** if the test question has the same wording as a training question, ignoring numbers, run the most common training program for that wording on the test question's numbers.
- **Rule 2 (nearest question):** otherwise, find the most similar training question with the same count of numbers (TF-IDF cosine similarity), copy its program and run it on the test question's numbers.

Ties are broken with a stable sort, so the results are the same on every machine.

## DeductReasoner

This step runs the [authors' code](https://github.com/allanj/Deductive-MWP) and their released checkpoint, a 502 MB download. It needs an older `transformers`, so use a separate environment. A GPU is recommended; on a CPU it takes much longer.

```bash
python -m venv .venv-deduct
source .venv-deduct/bin/activate
pip install -r deduct_reasoner/requirements.txt
python -m deduct_reasoner.run_checkpoint
```

Then go back to the main environment and compare:

```bash
source .venv/bin/activate
python -m deduct_reasoner.compare
```

## Expected results

Filtered split (value accuracy, %):

| Method | Test all | Test seen | Test new | Dev all | Dev seen | Dev new |
|---|---|---|---|---|---|---|
| Rule 1: lookup only | 71.21 | 99.74 | 0.00 | 70.43 | 99.76 | 0.00 |
| Rules 1 + 2 | 82.55 | 99.74 | 39.65 | 81.58 | 99.76 | 37.94 |
| DeductReasoner | 77.20 | 93.19 | 37.25 | 76.28 | 93.13 | 35.83 |

Full dataset (multiple-choice accuracy, %):

| Method | Test | Dev |
|---|---|---|
| Rule 1: lookup only | 55.04 | 55.11 |
| Rule 1 on seen questions | 71.47 | 72.25 |
| Rule 2 on new questions | 43.15 | 40.77 |
| Rules 1 + 2 | 64.96 | 64.78 |

Full dataset test set under stricter matching rules (%):

| Matching rule | Rules 1 + 2 | Reference programs | Random program |
|---|---|---|---|
| Closest option | 64.96 | 72.23 | 21.54 |
| Within 10% | 57.49 | 65.93 | 1.74 |
| Within 5% | 56.08 | 64.59 | 1.47 |
| Within 2% | 54.64 | 62.81 | 1.04 |
| Within 1% | 53.40 | 61.51 | 0.94 |
| Within 0.1% | 51.02 | 59.13 | 0.77 |

Splits with no shared templates (Rule 2): 40.24% on the filtered data and 41.84% on the full data.

## Notes

- **Interpreter for the full data:** MathQA publishes operation names but no formulas, so the formulas in `src/interpreter.py` are written from the names and checked against the training data. `log` uses base 2, on weak evidence, and `sine` and `tangent` are not implemented. These choices change the scores very little.
- **Full-dataset comparison:** the 54.2% in the original MathQA paper is quoted, not rerun, and that paper does not state its matching threshold. The stricter matching rules above show how the comparison depends on this.

## Data

The data is not stored in this repository. The filtered split comes from [Deductive-MWP](https://github.com/allanj/Deductive-MWP) and the full dataset from the [MathQA website](https://math-qa.github.io/math-QA/).
