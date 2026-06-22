#!/usr/bin/env bash
# Status check. Usage: bash scripts/check_blast.sh
set -euo pipefail

source "$(dirname "$0")/config_paths.sh"

SUMMARY="$OUT/results/${NAME}_hits.summary.tsv"
RAW="$OUT/results/${NAME}_hits.raw.tsv"

bar() { printf '%s\n' "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; }

bar
if [[ -f "$OUT/blast.done" ]]; then
  echo "  STATUS      ✅ DONE"
else
  echo "  STATUS      🔄 not finished (no blast.done)"
fi
bar
echo "  Queries     $NQUERY in resources/queries.fasta"
[[ -f "$RAW" ]] && echo "  Raw hits    $(wc -l < "$RAW" | tr -d ' ') alignments"
[[ -f "$SUMMARY" ]] && echo "  Summary     $(($(wc -l < "$SUMMARY") - 1)) queries annotated"
echo "  output_dir  $OUT"
bar
