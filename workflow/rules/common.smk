# Shared helpers (aligned with index_Trep_refs / Trep_pangenome).

from pathlib import Path


def asm(file_name):
    return Path(file_name.replace(".gz", "")).stem


def ref_fna(target, refs_dir, use_hap_subdir=False):
    """Indexed FASTA from index_Trep_refs: {refs_dir}/{source}/[{subdir}/]{assembly}.fna."""
    base = Path(refs_dir) / target["source"]
    if use_hap_subdir:
        base = base / target["results_subdir"]
    return base / f"{asm(target['file'])}.fna"
