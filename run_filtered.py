"""Repetition and copy-baseline results on the filtered MathQA split.

    python run_filtered.py
"""
from collections import Counter

import numpy as np

from src.baseline import CopyBaseline, share_in_repeated_templates, template_disjoint_split
from src.datasets import FilteredDataset, clean_text
from src.utils import load_filtered, percent, save_results

SIMILARITY_BANDS = ((0.0, 0.5), (0.5, 0.7), (0.7, 0.85), (0.85, 1.01))


def repetition(dataset, data):
    train_texts = {clean_text(r) for r in data["train"]}
    train_templates = Counter(dataset.template(r) for r in data["train"])
    output = {"train_problems": len(data["train"]), "distinct_train_templates": len(train_templates)}
    print(f"Training problems {len(data['train']):,} | distinct templates {len(train_templates):,}")
    for split in ("test", "dev"):
        records = data[split]
        exact = sum(clean_text(r) in train_texts for r in records)
        same = sum(dataset.template(r) in train_templates for r in records)
        output[split] = {"exact_copies": exact, "same_template": same, "percent": percent(same, len(records))}
        print(f"{split:4s}: exact copies {exact} of {len(records):,} | same template {same:,} ({percent(same, len(records)):.1f}%)")
    pooled = data["train"] + data["dev"] + data["test"]
    share, templates = share_in_repeated_templates(dataset, pooled)
    output["share_in_template_seen_twice"] = share
    print(f"All {len(pooled):,} problems: {templates:,} templates, {share:.1f}% in a template that occurs at least twice")
    return output


def main():
    dataset = FilteredDataset()
    data = load_filtered()

    print("=== Repetition ===")
    results = {"repetition": repetition(dataset, data)}

    print("\n=== Copy baseline (value accuracy) ===")
    baseline = CopyBaseline(dataset, data["train"])
    for split in ("test", "dev"):
        evaluation = baseline.evaluate(data[split])
        seen, new, n = evaluation.seen, ~evaluation.seen, len(evaluation.right)
        results[split] = {
            "rule1_all": percent(evaluation.lookup_right(), n),
            "seen": evaluation.accuracy(seen),
            "rule2_new": evaluation.accuracy(new),
            "rules_1_and_2_all": evaluation.accuracy(),
            "right": int(evaluation.right.sum()),
            "total": n,
        }
        print(f"{split.upper():4s}: Rule 1 {results[split]['rule1_all']:.2f}% | seen {results[split]['seen']:.2f}% "
              f"| Rule 2 on new {results[split]['rule2_new']:.2f}% ({int(evaluation.right[new].sum())}/{int(new.sum())}) "
              f"| Rules 1 + 2 {results[split]['rules_1_and_2_all']:.2f}% ({results[split]['right']}/{n})")

        if split == "test":
            print("\nRule 2 on new test questions, by similarity to the copied question:")
            near = evaluation.similarity[new] >= 0.85
            results["new_test_near_duplicates_percent"] = 100 * float(near.mean())
            results["rule2_by_similarity"] = []
            for low, high in SIMILARITY_BANDS:
                band = new & (evaluation.similarity >= low) & (evaluation.similarity < high)
                results["rule2_by_similarity"].append({"low": low, "questions": int(band.sum()), "accuracy": evaluation.accuracy(band)})
                print(f"  {low:.2f} to {min(high, 1.0):.2f}: {int(band.sum()):4d} questions, {evaluation.accuracy(band):.1f}% right")
            print(f"Similarity of at least 0.85: {100 * float(near.mean()):.1f}% of new test questions\n")

    print("\n=== Split with no shared templates ===")
    pooled = data["train"] + data["dev"] + data["test"]
    clean_train, clean_test = template_disjoint_split(dataset, pooled, len(data["test"]))
    clean_right = [dataset.is_right(value, r) for (value, _), r in zip(CopyBaseline(dataset, clean_train).nearest_values(clean_test), clean_test)]
    results["template_disjoint"] = {"test_problems": len(clean_test), "rule2": 100 * float(np.mean(clean_right))}
    print(f"Rule 2: {results['template_disjoint']['rule2']:.2f}% on {len(clean_test):,} test problems")

    save_results("filtered", results)


if __name__ == "__main__":
    main()
