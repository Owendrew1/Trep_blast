#!/usr/bin/env python3
"""Summarize BLAST hits per query with coverage-based hit/deletion calls."""

import argparse
import csv
from collections import defaultdict
from pathlib import Path


FIELDS = [
    "qseqid",
    "sseqid",
    "pident",
    "length",
    "qstart",
    "qend",
    "sstart",
    "send",
    "evalue",
    "bitscore",
    "qcovs",
]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hits", required=True, help="BLAST outfmt6 TSV (may be empty).")
    p.add_argument("--queries", required=True, help="Query FASTA used for blastn.")
    p.add_argument("--output", required=True, help="Annotated summary TSV.")
    p.add_argument("--min-pident", type=float, default=80.0)
    p.add_argument("--min-qcov", type=float, default=70.0)
    p.add_argument("--max-evalue", type=float, default=1e-5)
    return p.parse_args()


def load_query_ids(path):
    ids = []
    with open(path) as f:
        for line in f:
            if line.startswith(">"):
                ids.append(line[1:].strip().split()[0])
    return ids


def load_hits(path):
    by_query = defaultdict(list)
    p = Path(path)
    if not p.is_file() or p.stat().st_size == 0:
        return by_query
    with open(p) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) < len(FIELDS):
                raise ValueError(f"Expected {len(FIELDS)} columns, got {len(cols)}: {line}")
            row = dict(zip(FIELDS, cols))
            row["pident"] = float(row["pident"])
            row["length"] = int(row["length"])
            row["qstart"] = int(row["qstart"])
            row["qend"] = int(row["qend"])
            row["sstart"] = int(row["sstart"])
            row["send"] = int(row["send"])
            row["evalue"] = float(row["evalue"])
            row["bitscore"] = float(row["bitscore"])
            row["qcovs"] = float(row["qcovs"])
            by_query[row["qseqid"]].append(row)
    return by_query


def ref_coords(sstart, send):
    return min(sstart, send), max(sstart, send)


def classify(hit, min_pident, min_qcov, max_evalue):
    if hit["evalue"] > max_evalue:
        return "weak_evalue"
    if hit["qcovs"] < min_qcov:
        return "low_coverage"
    if hit["pident"] < min_pident:
        return "low_identity"
    return "hit"


def deletion_candidate(status):
    return status in {"no_hit", "low_coverage", "weak_evalue"}


def summarize(query_ids, hits_by_query, min_pident, min_qcov, max_evalue):
    out = []
    for qid in query_ids:
        hits = hits_by_query.get(qid, [])
        if not hits:
            out.append(
                {
                    "query_id": qid,
                    "status": "no_hit",
                    "deletion_candidate": "yes",
                    "subject_id": ".",
                    "ref_start": ".",
                    "ref_end": ".",
                    "strand": ".",
                    "pident": ".",
                    "qcovs": ".",
                    "align_length": ".",
                    "evalue": ".",
                    "bitscore": ".",
                }
            )
            continue

        best = max(hits, key=lambda h: (h["bitscore"], h["qcovs"], h["pident"]))
        start, end = ref_coords(best["sstart"], best["send"])
        strand = "+" if best["sstart"] <= best["send"] else "-"
        status = classify(best, min_pident, min_qcov, max_evalue)
        out.append(
            {
                "query_id": qid,
                "status": status,
                "deletion_candidate": "yes" if deletion_candidate(status) else "no",
                "subject_id": best["sseqid"],
                "ref_start": start,
                "ref_end": end,
                "strand": strand,
                "pident": best["pident"],
                "qcovs": best["qcovs"],
                "align_length": best["length"],
                "evalue": best["evalue"],
                "bitscore": best["bitscore"],
            }
        )
    return out


def main():
    args = parse_args()
    query_ids = load_query_ids(args.queries)
    hits_by_query = load_hits(args.hits)
    rows = summarize(query_ids, hits_by_query, args.min_pident, args.min_qcov, args.max_evalue)

    fieldnames = [
        "query_id",
        "status",
        "deletion_candidate",
        "subject_id",
        "ref_start",
        "ref_end",
        "strand",
        "pident",
        "qcovs",
        "align_length",
        "evalue",
        "bitscore",
    ]
    with open(args.output, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
