# Paths, config-derived constants, and helpers (aligned with Trep_pangenome / Giraffe_vg).

from pathlib import Path


def asm(file_name):
    return Path(file_name.replace(".gz", "")).stem


def ref_fna(target, refs_dir, use_hap_subdir=False):
    """Indexed FASTA from index_Trep_refs: {refs_dir}/{source}/[{subdir}/]{assembly}.fna."""
    base = Path(refs_dir) / target["source"]
    if use_hap_subdir:
        base = base / target["results_subdir"]
    return base / f"{asm(target['file'])}.fna"


REFS = config["refs_dir"]
INDEX_DONE = config["index_done_flag"]
USE_HAP_SUBDIR = config.get("refs_use_haplotype_subdir", False)
TARGET = config["blast_target"]
OUT = Path(config["output_dir"])
LOG = OUT / "blast_logs"
RES = OUT / "results"
DONE = OUT / "blast.done"
CONDA = "envs/blast.yaml"

BLAST = config["blast"]
QUERY_FASTA = config["queries_fasta"]
NAME = TARGET["name"]

REF = ref_fna(TARGET, REFS, USE_HAP_SUBDIR)
DB_DIR = OUT / "db" / NAME
DB_PREFIX = DB_DIR / REF.name
RAW_HITS = RES / f"{NAME}_hits.raw.tsv"
SUMMARY = RES / f"{NAME}_hits.summary.tsv"
PARSE_SCRIPT = Path(workflow.basedir) / "scripts" / "parse_blast_hits.py"
