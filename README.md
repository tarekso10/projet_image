# Comparative RAG for Image Captioning

Reproducible baseline-versus-dense-RAG study for MS COCO. The implementation uses BLIP for caption generation and CLIP image embeddings for image-to-image evidence retrieval. Each retrieved training image contributes its original human captions as evidence. The pipeline excludes self-retrieval and checks split IDs before processing.

## Scope and assumptions

The brief does not state the assigned group or provide the instructors' frozen split IDs. This repository implements **Naive/Dense RAG** as a configurable starting technique. Its local split is deterministic, but it is not a substitute for the course-wide stratified split. Put the shared validation/test IDs in `data/splits/validation_ids.txt` and `data/splits/test_ids.txt` before preparing data. The brief specifies both 100 and 1,000 test images in different sections; the common dataset section says 100, which is the default here. Change `config/default.yaml` only to match an instructor decision.

This workspace did not contain COCO data or model weights. Consequently, no experimental results are claimed yet. The report template records the required methods and pending result slots. COCO downloads and model checkpoints are large; source data and generated outputs are excluded from Git.

## Setup

Python 3.10+ is required. In a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[models,metrics]"
```

The `models` extra installs PyTorch, Transformers, Sentence Transformers, and FAISS. The current runner uses exact cosine search in NumPy for reproducibility; FAISS is available for scaling beyond the 10,000-image course subset. The `metrics` extra installs COCO caption scorers. SPICE may require a Java runtime. Select a compatible CPU or CUDA PyTorch build for the available hardware.

## Data layout and preparation

Download the COCO 2017 images and captions/instances annotations from the [official COCO site](https://cocodataset.org/#download). Place them as follows (image archive extraction is intentionally manual to avoid unexpectedly downloading multiple gigabytes):

```text
data/raw/train2017/                 # COCO train2017 images
data/raw/val2017/                   # COCO val2017 images
data/annotations/captions_train2017.json
data/annotations/captions_val2017.json
data/annotations/instances_train2017.json
data/annotations/instances_val2017.json
```

Run preprocessing after adding the shared split files:

```powershell
caption-rag prepare `
  --train-annotations data/annotations/captions_train2017.json `
  --train-images data/raw/train2017 `
  --val-annotations data/annotations/captions_val2017.json `
  --val-images data/raw/val2017
```

If shared ID files are absent, the command makes deterministic, disjoint validation and test subsets of the configured sizes and writes their IDs under `data/splits/`. That is useful for a smoke-sized local run, but results should not be submitted as course-comparable results. The preprocessing audit fails on duplicate IDs, missing image files, missing captions, caption-count mismatches, or split overlap. Training uses 10,000 images by default; `--train-count` supports a smaller development run.

## Run the experiment

```powershell
caption-rag run
```

This creates one BLIP baseline caption and one BLIP caption prompted with top-k CLIP-image-retrieved training captions for each test image. Outputs are `outputs/captions.jsonl`, the saved knowledge image embeddings, and aggregate COCO metrics. Each JSONL record stores the image ID, method, generated caption, raw references, and retrieved IDs/scores. Keep raw evaluation references out of all retrieval indexes and prompts.

The initial runner is the minimal main comparison. The protocol still requires tuning, per-image statistical comparisons, hallucination coding, uncertainty analysis, ablations, and qualitative examples before a final report can make claims. Never infer or invent results for unrun experiments.

## Dataset exploration

The exploration function can be run from Python once the standard COCO annotation files are available:

```powershell
python -c "from caption_rag.exploration import explore; explore('data/annotations/instances_train2017.json','data/annotations/captions_train2017.json','outputs/dataset_stats')"
```

It produces top object counts, scene-complexity and caption-length histograms, token vocabulary size, and a JSON summary. POS tagging and indoor/outdoor, day/night, color, and relation analyses need an explicitly selected tagger/metadata source; these are not guessed from the image captions.

## Reproducibility

- Record the Python, PyTorch, Transformers, model checkpoint revision, device, and CUDA versions in the final report.
- Keep the provided split ID files unchanged; record hashes in the experiment log.
- Save all outputs and configurations with each run. Record retrieval metric, top-k, latency, embedding dimensions, and model revisions.
- Use validation data for tuning only. Do not use test captions for retrieval, prompt construction, or model selection.
- Report per-image scores so paired tests can be performed. Apply Shapiro-Wilk to paired score differences; select paired t-test or Wilcoxon signed-rank as specified in the brief, with Bonferroni correction and effect sizes.

## Repository layout

```text
config/default.yaml          Run configuration
src/caption_rag/data.py       COCO loading and leakage audit
src/caption_rag/models.py     CLIP and BLIP model wrappers
src/caption_rag/retrieval.py  Exact cosine dense index
src/caption_rag/metrics.py    COCO metrics and paired tests
src/caption_rag/exploration.py Dataset descriptive statistics
src/caption_rag/cli.py        prepare/run commands
report/REPORT.md              English report draft and results checklist
```
