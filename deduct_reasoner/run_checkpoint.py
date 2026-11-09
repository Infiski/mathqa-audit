"""Run the released DeductReasoner MathQA checkpoint on the filtered test and dev sets.

Needs its own environment (see deduct_reasoner/requirements.txt). A GPU is recommended.

    python -m deduct_reasoner.run_checkpoint

Writes results/deduct_reasoner/mathqa_{test,dev}.res.json for deduct_reasoner.compare to score.
"""
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "deduct_reasoner" / "Deductive-MWP"
OUTPUT = ROOT / "results" / "deduct_reasoner"

REPO_URL = "https://github.com/allanj/Deductive-MWP"
COMMIT = "bb243bf6481f7ac7d8f67413b655ec564b98fe5e"   # the version these results were measured with
CHECKPOINT_ID = "1hgqSZwMyFearr_RJebL51ROflqwdsZUv"   # Google Drive file released by the authors


def setup():
    if not REPO.exists():
        print("Cloning Deductive-MWP")
        subprocess.run(["git", "clone", "-q", REPO_URL, str(REPO)], check=True)
        subprocess.run(["git", "checkout", "-q", COMMIT], cwd=REPO, check=True)
    (REPO / "results").mkdir(exist_ok=True)
    models = REPO / "model_files"
    models.mkdir(exist_ok=True)
    if not (models / "mathqa" / "pytorch_model.bin").exists():
        print("Downloading the checkpoint (502 MB)")
        subprocess.run(["gdown", CHECKPOINT_ID], cwd=models, check=True)
        with zipfile.ZipFile(models / "mathqa.zip") as archive:
            archive.extractall(models)


def run_split(split, device):
    data = "data/MathQA/mathqa_{}_nodup_our_filtered.json"
    command = [
        sys.executable, "universal_main.py", f"--device={device}", "--model_folder=mathqa", "--mode=test",
        "--height=10", "--train_max_height=15", f"--train_file={data.format('train')}", f"--test_file={data.format(split)}",
        "--batch_size=32", "--var_update_mode=gru", "--bert_model_name=roberta-base", "--fp16=0",
    ]
    print(f"Running on {split} ({device})", flush=True)
    finished = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    log = finished.stdout + finished.stderr
    (OUTPUT / f"{split}.log").write_text(log)
    if finished.returncode != 0:
        print("\n".join(log.splitlines()[-30:]))
        sys.exit(f"DeductReasoner failed on {split}; the full log is in {OUTPUT / (split + '.log')}")
    for line in log.splitlines():
        if "Value accuracy" in line or "removed:" in line:
            print(" ", line.split(" - ")[-1], flush=True)
    shutil.copy(REPO / "results" / "mathqa.res.json", OUTPUT / f"mathqa_{split}.res.json")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    setup()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    for split in ("test", "dev"):
        run_split(split, device)
    print("Done. Now run: python -m deduct_reasoner.compare")


if __name__ == "__main__":
    main()
