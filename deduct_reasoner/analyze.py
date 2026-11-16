"""Where DeductReasoner is right and wrong, compared with the training programs.

Run deduct_reasoner.run_checkpoint first, then:

    python -m deduct_reasoner.analyze
    python -m deduct_reasoner.analyze --split dev --examples 8

For each test question it compares the model's steps with
  - seen wording: the most common training program for the same template, run on the test numbers
  - new wording:  the program of the most similar training question (Rule 2, TF-IDF), run on the test numbers
  - wrong answers: the reference program, to say what went wrong.

Counts are saved in results/deduct_reasoner_analysis_<split>.json and
examples in results/examples/deduct_reasoner_<split>.md.
"""
import argparse
import json
import random
from collections import Counter

from deduct_reasoner.compare import is_right, load_predictions
from src.baseline import CopyBaseline
from src.datasets import FilteredDataset
from src.utils import RESULTS, load_filtered, save_results


OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b if b else float("nan"),
    "^": lambda a, b: a ** b,
}


def ground(steps, numbers):
    """Run a filtered-split program and return its steps as (left, right, op, result), as the authors' code does."""
    results, grounded = [], []

    def value(token):
        if token.startswith("m_"):
            return results[int(token[2:]) - 1]
        if len(token) == 1 and token.isalpha():
            return numbers[ord(token) - ord("a")]
        return float(token)

    try:
        for left, right, op in steps:
            a, b = value(left), value(right)
            if op.endswith("_rev"):
                a, b, op = b, a, op[:-4]
            result = OPERATIONS[op](a, b)
            results.append(result)
            grounded.append([a, b, op, result])
    except (IndexError, OverflowError, KeyError):
        return None
    return grounded


def unreverse(grounded):
    """The authors' output sometimes keeps "_rev" (b op a) in a step; write every step as a op b."""
    output = []
    for a, b, op, result in grounded:
        if op.endswith("_rev"):
            a, b, op = b, a, op[:-4]
        output.append((float(a), float(b), op, float(result)))
    return output


def normalise(grounded):
    """Steps as comparable tuples. a + b and b + a count as the same step, and so do a * b and b * a."""
    if grounded is None:
        return None
    output = []
    for a, b, op, _ in unreverse(grounded):
        a, b = round(a, 6), round(b, 6)
        if op in "+*":
            a, b = sorted((a, b))
        output.append((a, b, op))
    return tuple(output)


def show(grounded):
    if not grounded:
        return "(none)"
    return "; ".join(f"{a:g} {op} {b:g} = {r:g}" for a, b, op, r in unreverse(grounded))


def why_wrong(predicted, gold):
    """A short reason, from comparing the model's steps with the reference steps."""
    if predicted is None:
        return "no prediction (dropped by the data loader)"
    if gold is None:
        return "reference program cannot be run"
    p, g = normalise(predicted), normalise(gold)
    if len(p) < len(g):
        return "too few steps"
    if len(p) > len(g):
        return "too many steps"
    if [s[2] for s in p] != [s[2] for s in g]:
        return "same number of steps, different operations"
    return "same operations, different numbers or order"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--split", default="test", choices=("test", "dev"))
    parser.add_argument("--examples", type=int, default=5, help="examples to show for each group")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    dataset = FilteredDataset()
    data = load_filtered()
    train, records = data["train"], data[args.split]
    predictions = load_predictions(args.split)
    baseline = CopyBaseline(dataset, train)

    # every training program for each template, and the training question it came from
    programs_by_template = {}
    for r in train:
        programs_by_template.setdefault(dataset.template(r), []).append(r)

    new_records = [r for r in records if not baseline.is_seen(r)]
    nearest = {r["id"]: train[j] if j is not None else None for r, (j, _) in zip(new_records, baseline.nearest(new_records))}

    rows = []
    for r in records:
        prediction = predictions.get(r["id"])
        predicted = prediction.get("pred_ground_equation") if prediction else None
        gold = ground(r["equation_layer"], r["num_list"])
        seen = baseline.is_seen(r)
        right = is_right(prediction)
        if seen:
            twins = programs_by_template[dataset.template(r)]
            top_program = baseline.lookup_table[dataset.template(r)].most_common(1)[0][0]
            source = next(t for t in twins if dataset.program_key(t) == top_program)
            copied = ground(source["equation_layer"], r["num_list"])
            all_copied = {normalise(ground(t["equation_layer"], r["num_list"])) for t in twins}
        else:
            source = nearest[r["id"]]
            copied = ground(source["equation_layer"], r["num_list"]) if source else None
            all_copied = {normalise(copied)}
        rows.append({
            "record": r, "seen": seen, "right": right, "dropped": prediction is None,
            "predicted": predicted, "gold": gold, "source": source, "copied": copied,
            "same_as_copied": predicted is not None and normalise(predicted) == normalise(copied),
            "same_as_any_training_program": predicted is not None and normalise(predicted) in all_copied,
            "copy_right": baseline.lookup_value(r) is not None and dataset.is_right(baseline.lookup_value(r), r) if seen
            else copied is not None and dataset.is_right(copied[-1][3], r),
            "why": None if right else why_wrong(predicted, gold),
            "steps": len(r["equation_layer"]),
        })

    groups = {
        "right_seen": [x for x in rows if x["right"] and x["seen"]],
        "right_new": [x for x in rows if x["right"] and not x["seen"]],
        "wrong_seen": [x for x in rows if not x["right"] and x["seen"]],
        "wrong_new": [x for x in rows if not x["right"] and not x["seen"]],
    }
    results = {"split": args.split, "questions": len(rows)}
    print(f"DeductReasoner on the filtered {args.split} set ({len(rows)} questions)\n")
    for name, group in groups.items():
        live = [x for x in group if not x["dropped"]]
        summary = {
            "questions": len(group),
            "dropped": len(group) - len(live),
            "same_steps_as_copied_program": sum(x["same_as_copied"] for x in live),
            "same_steps_as_any_training_program_for_template": sum(x["same_as_any_training_program"] for x in live),
            "copy_baseline_right": sum(x["copy_right"] for x in group),
        }
        first_steps = Counter(show(x["predicted"][:1]).rsplit(" = ", 1)[0] for x in live)
        summary["most_common_first_steps"] = dict(first_steps.most_common(3))
        if name.startswith("wrong"):
            summary["why"] = dict(Counter(x["why"] for x in group).most_common())
            summary["gold_steps_of_dropped"] = dict(sorted(Counter(x["steps"] for x in group if x["dropped"]).items()))
        results[name] = summary
        compared = "the most common training program for its template" if "seen" in name else "the nearest training question's program (TF-IDF)"
        print(f"{name.replace('_', ' ')}: {len(group)} questions ({summary['dropped']} dropped)")
        print(f"  model's steps are the same as {compared}: {summary['same_steps_as_copied_program']} of {len(live)}")
        print(f"  copy baseline is right on: {summary['copy_baseline_right']} of {len(group)}")
        print("  model's most common first steps: " + ", ".join(f"{s} ({n})" for s, n in first_steps.most_common(3)))
        if "why" in summary:
            for reason, count in summary["why"].items():
                print(f"  {reason}: {count}")
        print()

    rng = random.Random(args.seed)
    lines = [f"# DeductReasoner examples (filtered {args.split} set)", ""]
    titles = {
        "right_seen": "Right, and the template is in training",
        "right_new": "Right, with new wording",
        "wrong_seen": "Wrong, although the template is in training",
        "wrong_new": "Wrong, with new wording",
    }
    for name, group in groups.items():
        lines += [f"## {titles[name]} ({len(group)} questions)", ""]
        pool = [x for x in group if not x["dropped"]] or group
        for x in sorted(rng.sample(pool, min(args.examples, len(pool))), key=lambda x: x["record"]["id"]):
            r = x["record"]
            lines += [f"**Test question {r['id']}**: {r['Problem']}",
                      f"- numbers: {r['num_list']}, reference value {x['gold'][-1][3]:g}" if x["gold"] else "",
                      f"- reference steps: {show(x['gold'])}"]
            if x["source"] is not None:
                label = "training question with the same template" if x["seen"] else "most similar training question (TF-IDF)"
                lines += [f"- {label}: {x['source']['Problem']}",
                          f"- its program on the test numbers: {show(x['copied'])}"]
            lines += [f"- DeductReasoner's steps: {show(x['predicted'])}",
                      f"- same steps as the training program: {'yes' if x['same_as_copied'] else 'no'}"]
            if x["why"]:
                lines.append(f"- what went wrong: {x['why']}")
            lines.append("")
    text = "\n".join(line for line in lines if line is not None)
    path = RESULTS / "examples" / f"deduct_reasoner_{args.split}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n")
    print(f"Saved {path}")
    save_results(f"deduct_reasoner_analysis_{args.split}", results)


if __name__ == "__main__":
    main()
