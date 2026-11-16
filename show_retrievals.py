"""Show which training question the copy baseline retrieves for test questions.

    python show_retrievals.py                      # filtered split, TF-IDF and BERT
    python show_retrievals.py --dataset full
    python show_retrievals.py --per-band 5 --seen 5 --no-bert

For new questions (template not in training), it shows the training question picked by Rule 2
with TF-IDF and with BERT sentence embeddings, the copied program and whether it gives the right
answer on the test question's numbers. Examples are drawn from each similarity band. For seen
questions it shows the training questions with the same template (Rule 1).

The examples are printed and saved in results/examples/retrieval_<dataset>.md.
"""
import argparse
import random

import numpy as np

from run_filtered import SIMILARITY_BANDS
from src.baseline import CopyBaseline
from src.datasets import FilteredDataset, FullDataset
from src.embeddings import DEFAULT_MODEL, EmbeddingBaseline
from src.utils import RESULTS, load_filtered, load_full

DATASETS = {"filtered": (FilteredDataset, load_filtered), "full": (FullDataset, load_full)}


def program_text(record):
    return record.get("equation") or record.get("linear_formula")


def reference_text(dataset, record):
    if isinstance(dataset, FullDataset):
        return f"correct option {record['correct']} ({record['options']})"
    return f"reference value {dataset.gold_value(record):g}"


def answer_text(dataset, value, record):
    mark = "right" if dataset.is_right(value, record) else "wrong"
    shown = "no value" if value is None else f"{value:g}"
    if isinstance(dataset, FullDataset) and value is not None:
        shown += f", closest option {dataset.choose_option(value, record)}"
    return f"{shown} -> **{mark}**"


def pick_lines(dataset, method, train, choice, similarity, record):
    if choice is None:
        return [f"- **{method}**: no training question with the same count of numbers in the top 50 -> **wrong**"]
    source = train[choice]
    value = dataset.run(dataset.program_key(source), record)
    return [f"- **{method}** (similarity {similarity:.3f}): {source['Problem']}",
            f"  - its program: `{program_text(source)}`",
            f"  - run on the test numbers: {answer_text(dataset, value, record)}"]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", default="filtered", choices=list(DATASETS))
    parser.add_argument("--per-band", type=int, default=3, help="new test questions to show from each similarity band")
    parser.add_argument("--seen", type=int, default=3, help="seen test questions to show (Rule 1)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="sentence-transformers model for the BERT column")
    parser.add_argument("--no-bert", action="store_true", help="show TF-IDF only")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    dataset_class, load = DATASETS[args.dataset]
    dataset, data = dataset_class(), load()
    train, test = data["train"], data["test"]
    tfidf = CopyBaseline(dataset, train)
    seen = np.array([tfidf.is_seen(r) for r in test])
    new_positions = np.flatnonzero(~seen)
    new_records = [test[i] for i in new_positions]

    picks = {"TF-IDF": tfidf.nearest(new_records)}
    if not args.no_bert:
        picks[f"BERT ({args.model.split('/')[-1]})"] = EmbeddingBaseline(dataset, train, args.model).nearest(new_records)
    tfidf_similarity = np.array([s for _, s in picks["TF-IDF"]])

    rng = random.Random(args.seed)
    lines = [f"# Retrieved training questions ({args.dataset} split, test set)", ""]

    lines += ["## New wording (Rule 2)", "",
              "Bands are by TF-IDF similarity to the picked training question.", ""]
    for low, high in SIMILARITY_BANDS:
        band = [k for k in range(len(new_records)) if low <= tfidf_similarity[k] < high]
        lines += [f"### TF-IDF similarity {low:.2f} to {min(high, 1.0):.2f} ({len(band)} new test questions)", ""]
        for k in sorted(rng.sample(band, min(args.per_band, len(band)))):
            record = new_records[k]
            lines += [f"**Test question {new_positions[k]}**: {record['Problem']}",
                      f"- {reference_text(dataset, record)}"]
            for method, chosen in picks.items():
                lines += pick_lines(dataset, method, train, *chosen[k], record)
            lines.append("")

    lines += ["## Seen wording (Rule 1)", ""]
    for i in sorted(rng.sample(list(np.flatnonzero(seen)), min(args.seen, int(seen.sum())))):
        record = test[i]
        twins = [r for r in train if dataset.template(r) == dataset.template(record)]
        value = tfidf.lookup_value(record)
        lines += [f"**Test question {i}**: {record['Problem']}",
                  f"- {reference_text(dataset, record)}",
                  f"- training questions with the same template: {len(twins)}"]
        lines += [f"  - {r['Problem']}" for r in twins[:3]]
        lines += [f"- most common training program run on the test numbers: {answer_text(dataset, value, record)}", ""]

    text = "\n".join(lines)
    print(text)
    path = RESULTS / "examples" / f"retrieval_{args.dataset}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n")
    print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
