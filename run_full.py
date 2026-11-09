"""Repetition and copy-baseline results on the full 37k MathQA dataset.

    python run_full.py
"""
import random
from collections import defaultdict

import numpy as np

from run_filtered import repetition
from src.baseline import CopyBaseline, template_disjoint_split
from src.datasets import FullDataset
from src.utils import load_full, percent, save_results

MATCHING_RULES = (("Closest option", None), ("Within 10%", 0.10), ("Within 5%", 0.05), ("Within 2%", 0.02), ("Within 1%", 0.01), ("Within 0.1%", 0.001))


def random_program_values(dataset, train, test, seed=0):
    """Run a random training program that needs the same count of numbers. A chance-level check."""
    by_count = defaultdict(list)
    for record in train:
        by_count[dataset.number_count(record)].append(dataset.program_key(record))
    rng = random.Random(seed)
    values = []
    for record in test:
        programs = by_count.get(dataset.number_count(record))
        values.append(dataset.run(rng.choice(programs), record) if programs else None)
    return values


def main():
    dataset = FullDataset()
    data = load_full()

    print("=== Repetition ===")
    results = {"repetition": repetition(dataset, data)}

    print("\n=== Copy baseline (multiple-choice accuracy, closest option) ===")
    baseline = CopyBaseline(dataset, data["train"])
    evaluations = {}
    for split in ("test", "dev"):
        evaluation = evaluations[split] = baseline.evaluate(data[split])
        seen, new, n = evaluation.seen, ~evaluation.seen, len(evaluation.right)
        results[split] = {
            "rule1_all": percent(evaluation.lookup_right(), n),
            "rule1_seen": evaluation.accuracy(seen),
            "rule2_new": evaluation.accuracy(new),
            "rules_1_and_2_all": evaluation.accuracy(),
            "near_duplicates_percent_of_new": 100 * float((evaluation.similarity[new] >= 0.85).mean()),
        }
        print(f"{split.upper():4s}: Rule 1 {results[split]['rule1_all']:.2f}% | Rule 1 on seen {results[split]['rule1_seen']:.2f}% "
              f"| Rule 2 on new {results[split]['rule2_new']:.2f}% ({int(evaluation.right[new].sum())}/{int(new.sum())}) "
              f"| Rules 1 + 2 {results[split]['rules_1_and_2_all']:.2f}% | near-duplicates among new {results[split]['near_duplicates_percent_of_new']:.1f}%")

    test = data["test"]
    reference = [dataset.reference_value(r) for r in test]
    random_values = random_program_values(dataset, data["train"], test)

    print(f"\n=== Stricter matching rules ({len(test):,} test problems) ===")
    print(f"{'Matching rule':16s} {'Rules 1 + 2':>12s} {'Reference':>10s} {'Random':>8s}")
    results["matching_rules"] = {}
    for name, tolerance in MATCHING_RULES:
        row = [100 * float(np.mean([dataset.is_right(v, r, tolerance) for v, r in zip(values, test)]))
               for values in (evaluations["test"].values, reference, random_values)]
        results["matching_rules"][name] = {"rules_1_and_2": row[0], "reference": row[1], "random": row[2]}
        print(f"{name:16s} {row[0]:12.2f} {row[1]:10.2f} {row[2]:8.2f}")

    print("\n=== Split with no shared templates ===")
    pooled = data["train"] + data["dev"] + data["test"]
    clean_train, clean_test = template_disjoint_split(dataset, pooled, len(test))
    clean_right = [dataset.is_right(value, r) for (value, _), r in zip(CopyBaseline(dataset, clean_train).nearest_values(clean_test), clean_test)]
    results["template_disjoint"] = {"test_problems": len(clean_test), "rule2": 100 * float(np.mean(clean_right))}
    print(f"Rule 2: {results['template_disjoint']['rule2']:.2f}% on {len(clean_test):,} test problems")

    save_results("full", results)


if __name__ == "__main__":
    main()
