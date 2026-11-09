"""Score DeductReasoner on seen and new wording and compare it with the copy baseline.

Run deduct_reasoner.run_checkpoint first, then:

    python -m deduct_reasoner.compare
"""
import json
import math

import numpy as np

from src.baseline import CopyBaseline
from src.datasets import FilteredDataset
from src.significance import exact_mcnemar, paired_bootstrap
from src.utils import RESULTS, load_filtered, save_results


def load_predictions(split):
    path = RESULTS / "deduct_reasoner" / f"mathqa_{split}.res.json"
    if not path.exists():
        raise SystemExit(f"{path} not found. Run: python -m deduct_reasoner.run_checkpoint")
    return {r["id"]: r for r in json.loads(path.read_text())}


def is_right(prediction):
    """Problems the model's loader dropped have no prediction and count as wrong, as in the authors' code."""
    if prediction is None or prediction.get("predict_value") is None or prediction.get("gold_value") is None:
        return False
    predicted, gold = float(prediction["predict_value"]), float(prediction["gold_value"])
    return not (math.isnan(predicted) or math.isnan(gold)) and abs(predicted - gold) < 1e-4


def main():
    dataset = FilteredDataset()
    data = load_filtered()
    baseline = CopyBaseline(dataset, data["train"])
    results = {}

    for split in ("test", "dev"):
        records = data[split]
        predictions = load_predictions(split)
        model = np.array([is_right(predictions.get(r["id"])) for r in records], dtype=bool)
        kept = np.array([r["id"] in predictions for r in records], dtype=bool)
        copy = baseline.evaluate(records)
        seen, new = copy.seen, ~copy.seen

        results[split] = {
            "deduct_reasoner_all": 100 * float(model.mean()),
            "deduct_reasoner_seen": 100 * float(model[seen].mean()),
            "deduct_reasoner_new": 100 * float(model[new].mean()),
            "copy_baseline_all": copy.accuracy(),
            "predicted": int(kept.sum()),
            "dropped": int((~kept).sum()),
        }
        print(f"{split.upper()} ({int(kept.sum())} predicted, {int((~kept).sum())} dropped and counted wrong)")
        print(f"  DeductReasoner: all {results[split]['deduct_reasoner_all']:.2f}% ({int(model.sum())}/{len(model)}) "
              f"| seen {results[split]['deduct_reasoner_seen']:.2f}% ({int(model[seen].sum())}/{int(seen.sum())}) "
              f"| new {results[split]['deduct_reasoner_new']:.2f}% ({int(model[new].sum())}/{int(new.sum())})")
        print(f"  Copy baseline : all {copy.accuracy():.2f}% ({int(copy.right.sum())}/{len(model)})")

        if split == "test":
            only_copy = int((copy.right & ~model).sum())
            only_model = int((~copy.right & model).sum())
            low, high = paired_bootstrap(copy.right, model)
            gap = 100 * float(copy.right.mean() - model.mean())
            only_copy_new = int((copy.right & ~model & new).sum())
            only_model_new = int((~copy.right & model & new).sum())
            results["test_comparison"] = {
                "gap_points": gap, "bootstrap_95_low": low, "bootstrap_95_high": high,
                "only_copy_right": only_copy, "only_model_right": only_model, "mcnemar_p": exact_mcnemar(only_copy, only_model),
                "kept_copy": 100 * float(copy.right[kept].mean()), "kept_model": 100 * float(model[kept].mean()),
                "new_copy_right": int(copy.right[new].sum()), "new_model_right": int(model[new].sum()),
                "new_mcnemar_p": exact_mcnemar(only_copy_new, only_model_new),
                "correct_answers_from_seen": int(model[seen].sum()),
            }
            c = results["test_comparison"]
            print(f"  Gap {gap:.2f} points (95% bootstrap interval {low:.2f} to {high:.2f})")
            print(f"  Only baseline right {only_copy} | only DeductReasoner right {only_model} | exact McNemar p = {c['mcnemar_p']:.2e}")
            print(f"  On the {int(kept.sum())} problems the model keeps: baseline {c['kept_copy']:.2f}%, DeductReasoner {c['kept_model']:.2f}%")
            print(f"  New wording: baseline {c['new_copy_right']} vs DeductReasoner {c['new_model_right']} of {int(new.sum())}, exact McNemar p = {c['new_mcnemar_p']:.3f}")
        print()

    save_results("deduct_reasoner_comparison", results)


if __name__ == "__main__":
    main()
