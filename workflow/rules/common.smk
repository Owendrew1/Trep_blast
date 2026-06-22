# Shared helpers for workflow/Snakefile.

from pathlib import Path


def asm(file_name):
    return Path(file_name.replace(".gz", "")).stem


def ref_fna(target, refs_dir):
    base = Path(refs_dir) / target["source"]
    return base / f"{asm(target['file'])}.fna"
