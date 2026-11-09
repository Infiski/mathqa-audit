"""The copy baseline: two rules and no learned weights.

Rule 1 (lookup): if the question's template is in training, run the most common training program
                 for that template on the question's numbers.
Rule 2 (nearest question): otherwise copy the program of the most similar training question that
                 has the same count of numbers.

The sort is stable so that ties between equally similar questions always break the same way.
"""
import random
from collections import Counter, defaultdict
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

TOP_K = 50


@dataclass
class Evaluation:
    values: list          # the baseline's answer for each question (None if it has none)
    seen: np.ndarray      # True if the question's template is in training
    right: np.ndarray     # True if the answer is correct
    similarity: np.ndarray  # similarity of the copied question (new questions only, otherwise NaN)

    def accuracy(self, mask=None):
        mask = np.ones(len(self.right), dtype=bool) if mask is None else mask
        return 100 * float(self.right[mask].mean())

    def lookup_right(self):
        return int(self.right[self.seen].sum())


class CopyBaseline:
    def __init__(self, dataset, train):
        self.dataset = dataset
        self.train = train
        self.lookup_table = defaultdict(Counter)
        for record in train:
            self.lookup_table[dataset.template(record)][dataset.program_key(record)] += 1

    def is_seen(self, record):
        return self.dataset.template(record) in self.lookup_table

    def lookup_value(self, record):
        programs = self.lookup_table.get(self.dataset.template(record))
        if programs is None:
            return None
        return self.dataset.run(programs.most_common(1)[0][0], record)

    def nearest_values(self, questions):
        """Rule 2. Returns a list of (value, similarity), one per question."""
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        train_vectors = vectorizer.fit_transform([self.dataset.template(r) for r in self.train])
        question_vectors = vectorizer.transform([self.dataset.template(r) for r in questions])
        similarity = (question_vectors @ train_vectors.T).tocsr()

        output = []
        for i, record in enumerate(questions):
            scores = similarity.getrow(i).toarray().ravel()
            value, best = None, 0.0
            for j in np.argsort(-scores, kind="stable")[:TOP_K]:
                if self.dataset.number_count(self.train[j]) == self.dataset.number_count(record):
                    value = self.dataset.run(self.dataset.program_key(self.train[j]), record)
                    best = float(scores[j])
                    break
            output.append((value, best))
        return output

    def evaluate(self, records):
        seen = np.array([self.is_seen(r) for r in records], dtype=bool)
        values = [self.lookup_value(r) if s else None for r, s in zip(records, seen)]
        similarity = np.full(len(records), np.nan)

        new_positions = np.flatnonzero(~seen)
        neighbours = self.nearest_values([records[i] for i in new_positions])
        for i, (value, best) in zip(new_positions, neighbours):
            values[i] = value
            similarity[i] = best

        right = np.array([self.dataset.is_right(v, r) for v, r in zip(values, records)], dtype=bool)
        return Evaluation(values, seen, right, similarity)


def template_disjoint_split(dataset, records, test_size, seed=0):
    """Pool the problems and split them so that every template appears on only one side."""
    groups = defaultdict(list)
    for record in records:
        groups[dataset.template(record)].append(record)
    templates = list(groups)
    random.Random(seed).shuffle(templates)

    test, train = [], []
    for template in templates:
        (test if len(test) < test_size else train).extend(groups[template])
    return train, test


def share_in_repeated_templates(dataset, records):
    counts = Counter(dataset.template(r) for r in records)
    return 100 * sum(c for c in counts.values() if c >= 2) / len(records), len(counts)
