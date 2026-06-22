#!/usr/bin/env bash
# Run UTM haploid BLAST workflow. Usage: ./scripts/run_blast.sh [cores]
set -euo pipefail
cd "$(dirname "$0")/.."
exec snakemake -s workflow/Snakefile --directory workflow --cores "${1:-4}" -p --use-conda
