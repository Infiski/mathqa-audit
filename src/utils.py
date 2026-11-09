"""Paths, data downloads and small helpers used by every experiment."""
import io
import json
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILTERED = ROOT / "data" / "filtered"
DATA_FULL = ROOT / "data" / "full"
RESULTS = ROOT / "results"

FILTERED_URL = "https://raw.githubusercontent.com/allanj/Deductive-MWP/main/data/MathQA/mathqa_{}_nodup_our_filtered.json"
FULL_URL = "https://math-qa.github.io/math-QA/data/MathQA.zip"
SPLITS = ("train", "dev", "test")


def _read_splits(folder):
    return {split: json.loads((folder / f"{split}.json").read_text()) for split in SPLITS}


def load_filtered():
    """The 16,191 / 2,411 / 1,605 split released with DeductReasoner. Downloads it the first time."""
    DATA_FILTERED.mkdir(parents=True, exist_ok=True)
    for split in SPLITS:
        path = DATA_FILTERED / f"{split}.json"
        if not path.exists():
            print(f"Downloading filtered MathQA: {split}")
            urllib.request.urlretrieve(FILTERED_URL.format(split), path)
    return _read_splits(DATA_FILTERED)


def load_full():
    """The official 29,837 / 4,475 / 2,985 MathQA release. Downloads it the first time."""
    DATA_FULL.mkdir(parents=True, exist_ok=True)
    if not all((DATA_FULL / f"{split}.json").exists() for split in SPLITS):
        print("Downloading full MathQA")
        with urllib.request.urlopen(FULL_URL) as response:
            archive = zipfile.ZipFile(io.BytesIO(response.read()))
        for split in SPLITS:
            (DATA_FULL / f"{split}.json").write_bytes(archive.read(f"{split}.json"))
    return _read_splits(DATA_FULL)


def percent(part, whole):
    return 100 * float(part) / float(whole)


def save_results(name, results):
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / f"{name}.json"
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nSaved {path.relative_to(ROOT)}")
