"""Rule 2 with BERT-based sentence embeddings, next to the TF-IDF version.

    python run_embeddings.py
    python run_embeddings.py --models sentence-transformers/all-MiniLM-L6-v2 sentence-transformers/all-mpnet-base-v2

The first run downloads the embedding models from Hugging Face.
"""
import argparse

import numpy as np

from run_filtered import SIMILARITY_BANDS
from src.baseline import CopyBaseline, template_disjoint_split
from src.datasets import FilteredDataset, FullDataset
from src.embeddings import DEFAULT_MODEL, EmbeddingBaseline
from src.utils import load_filtered, load_full, save_results

DATASETS = {"filtered": (FilteredDataset, load_filtered), "full": (FullDataset, load_full)}


def score(dataset, baseline, data):
    """Accuracy of Rules 1 + 2 and of Rule 2 on new questions, for test and dev."""
    output, chosen = {}, {}
    for split in ("test", "dev"):
        records = data[split]
        evaluation = baseline.evaluate(records)
        new = ~evaluation.seen
        output[split] = {
            "rules_1_and_2_all": evaluation.accuracy(),
            "rule2_new": evaluation.accuracy(new),
            "rule2_new_right": int(evaluation.right[new].sum()),
            "new_questions": int(new.sum()),
            "near_duplicates_percent_of_new": 100 * float((evaluation.similarity[new] >= 0.85).mean()),
        }
        if split == "test":
            output["test_by_similarity"] = []
            for low, high in SIMILARITY_BANDS:
                band = new & (evaluation.similarity >= low) & (evaluation.similarity < high)
                output["test_by_similarity"].append({"low": low, "questions": int(band.sum()),
                                                     "accuracy": evaluation.accuracy(band) if band.any() else None})
            new_records = [r for r, s in zip(records, evaluation.seen) if not s]
            chosen["test"] = [j for j, _ in baseline.nearest(new_records)]
    return output, chosen


def template_disjoint(dataset, data, make_baseline):
    pooled = data["train"] + data["dev"] + data["test"]
    clean_train, clean_test = template_disjoint_split(dataset, pooled, len(data["test"]))
    values = make_baseline(clean_train).nearest_values(clean_test)
    right = [dataset.is_right(value, r) for (value, _), r in zip(values, clean_test)]
    return {"test_problems": len(clean_test), "rule2": 100 * float(np.mean(right))}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--models", nargs="+", default=[DEFAULT_MODEL], help="sentence-transformers model names")
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS), choices=list(DATASETS))
    args = parser.parse_args()

    results = {}
    for name in args.datasets:
        dataset_class, load = DATASETS[name]
        dataset, data = dataset_class(), load()
        methods = {"tfidf": lambda train: CopyBaseline(dataset, train)}
        for model in args.models:
            methods[model] = lambda train, model=model: EmbeddingBaseline(dataset, train, model)

        results[name] = {}
        chosen = {}
        for method, make_baseline in methods.items():
            print(f"\n=== {name}: Rule 2 with {method} ===", flush=True)
            output, chosen[method] = score(dataset, make_baseline(data["train"]), data)
            output["template_disjoint"] = template_disjoint(dataset, data, make_baseline)
            results[name][method] = output
            for split in ("test", "dev"):
                s = output[split]
                print(f"{split.upper():4s}: Rules 1 + 2 {s['rules_1_and_2_all']:.2f}% | Rule 2 on new {s['rule2_new']:.2f}% "
                      f"({s['rule2_new_right']}/{s['new_questions']}) | similarity >= 0.85 among new {s['near_duplicates_percent_of_new']:.1f}%")
            print("Rule 2 on new test questions, by similarity:")
            for band in output["test_by_similarity"]:
                accuracy = "-" if band["accuracy"] is None else f"{band['accuracy']:.1f}%"
                print(f"  from {band['low']:.2f}: {band['questions']:4d} questions, {accuracy} right")
            print(f"No shared templates: Rule 2 {output['template_disjoint']['rule2']:.2f}% "
                  f"on {output['template_disjoint']['test_problems']:,} test problems")

        for model in args.models:
            same = np.mean([a == b for a, b in zip(chosen["tfidf"]["test"], chosen[model]["test"])])
            results[name][model]["same_training_question_as_tfidf_percent"] = 100 * float(same)
            print(f"\n{name}: {model} picks the same training question as TF-IDF for {100 * same:.1f}% of new test questions")

    save_results("embeddings", results)


if __name__ == "__main__":
    main()
