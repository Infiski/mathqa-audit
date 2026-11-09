"""Two checks that a difference between two methods on the same questions is not just luck."""
from math import comb

import numpy as np


def exact_mcnemar(only_first_right, only_second_right):
    """Two-sided p-value. If the methods were equally good, each disagreement would be a coin flip."""
    total = only_first_right + only_second_right
    smaller = min(only_first_right, only_second_right)
    return min(1.0, 2 * sum(comb(total, i) for i in range(smaller + 1)) / 2 ** total)


def paired_bootstrap(first_right, second_right, samples=10000, seed=0):
    """95% interval for the accuracy gap, resampling the same questions for both methods."""
    rng = np.random.default_rng(seed)
    n = len(first_right)
    gaps = []
    for _ in range(samples):
        chosen = rng.integers(0, n, n)
        gaps.append(100 * (first_right[chosen].mean() - second_right[chosen].mean()))
    return float(np.percentile(gaps, 2.5)), float(np.percentile(gaps, 97.5))
