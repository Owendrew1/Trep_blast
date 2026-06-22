# Trep_blast

BLAST query sequences against **UTM haploid** from `index_Trep_refs`. Maps hits to reference coordinates and flags likely deletions using query-coverage thresholds.

## Prerequisites

1. UTM haploid indexed (`index_Trep_refs`). Scratch layout (default config):

   ```
   /scratch/references/trifolium/repens/UTM_Trep_v1.0/GCA_030408175.1_UTM_Trep_v1.0_genomic.fna
   /scratch/references/trifolium/repens/Trep_ref_indexing.done
   ```

   Old home layout: set `refs_use_haplotype_subdir: true` and point `refs_dir` / `index_done_flag` at `index_Trep_refs/results` (see commented lines in `config/config.yaml`).

2. Conda env:

   ```bash
   conda env create -f environment.yaml
   conda activate snakemake
   ```

## Setup

Edit `config/config.yaml` if needed:

- `refs_dir`, `index_done_flag`, `refs_use_haplotype_subdir` — reference paths (match `Trep_pangenome` / `index_Trep_refs`)
- `output_dir` — where BLAST DB and results are written (default `/scratch/odrew060/Trep_blast`)
- `blast.min_qcov`, `blast.min_pident`, `blast.max_evalue` — hit vs deletion thresholds

Put your sequences in `resources/queries.fasta`.

## Run

```bash
cd ~/github-repos/Trep_blast
./scripts/run_blast.sh 4
```

Resume / check status:

```bash
bash scripts/check_blast.sh
```

Dry run:

```bash
snakemake -s workflow/Snakefile --directory workflow --cores 1 -n -p --use-conda
```

## Outputs

Under `{output_dir}/`:

| Path | Description |
|------|-------------|
| `db/UTM_haploid/` | BLAST nucleotide database |
| `results/UTM_haploid_hits.raw.tsv` | Raw BLAST outfmt6 |
| `results/UTM_haploid_hits.summary.tsv` | Best hit per query + status |
| `blast.done` | Workflow complete |

### Summary TSV columns

| Column | Meaning |
|--------|---------|
| `query_id` | Query sequence name |
| `status` | `hit`, `no_hit`, `low_coverage`, `low_identity`, or `weak_evalue` |
| `deletion_candidate` | `yes` if `no_hit`, `low_coverage`, or `weak_evalue` |
| `subject_id` | Reference contig/chromosome |
| `ref_start`, `ref_end` | Coordinates on UTM haploid |
| `qcovs` | Query coverage (%) — primary deletion threshold |

## Status logic

- **hit** — passes `min_pident`, `min_qcov`, and `max_evalue`
- **no_hit** — no BLAST alignment
- **low_coverage** — best hit covers &lt; `min_qcov`% of query → likely deletion or major divergence
- **low_identity** — hit location but poor identity (review manually)
- **weak_evalue** — poor significance

## Layout

```text
Trep_blast/
├── environment.yaml          # Snakemake only
├── config/config.yaml
├── resources/queries.fasta
├── workflow/
│   ├── Snakefile             # rules only
│   ├── envs/blast.yaml       # blast+ (Snakemake --use-conda)
│   ├── rules/common.smk        # paths, helpers
│   └── scripts/parse_blast_hits.py
└── scripts/
    ├── run_blast.sh
    └── check_blast.sh
```
