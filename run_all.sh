#!/bin/bash
# Reproduce the repetition and copy-baseline results. DeductReasoner is a separate step: see README.md.
set -eo pipefail
cd "$(dirname "$0")"
python run_filtered.py
echo
python run_full.py
