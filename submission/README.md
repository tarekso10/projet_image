# Phase 1 Submission Package

This package organizes the existing Phase 1 work into the four requested categories. It preserves the original source code, frozen split manifests, saved analyses, embeddings/indexes, QC evidence, and final report; it does not implement Phase 2 or change the scientific method.

## Contents

- `1_Source_Code/` ? Python entry point and modules, requirements, configuration, installation and CLI notes.
- `2_Dataset_Information/` ? MS COCO description, selection report, frozen manifests, selected reference captions, metadata, and dataset statistics.
- `3_Results/` ? exploration figures/statistics, preprocessing evidence, saved image/text embeddings, train-only FAISS indexes, retrieval outputs, and QC/compliance audits.
- `4_Final_Report/` ? latest verified PDF and active LaTeX source, bibliography, tables, and figures.
- `SUBMISSION_AUDIT.md` ? artifact inventory, exclusions, and verification findings.

## Installation and commands

Install dependencies from the source folder with `python -m pip install -r 1_Source_Code/requirements.txt`. Install spaCy's English model with `python -m spacy download en_core_web_sm` for POS analysis. Run `python main.py --help` from `1_Source_Code/` to see supported commands. A complete rerun also needs MS COCO 2017 images/annotations in configured paths and local model checkpoints; these are not bundled. Do not run selection/preprocessing on the frozen completed project.

## Principal evidence

- `3_Results/quality_control/final_quality_control.json` ? pipeline QC PASS for implemented checks.
- `3_Results/quality_control/phase1_final_compliance.json` and Markdown report ? overall requirement compliance PARTIAL. These statuses have different scopes.
- `3_Results/retrieval/` ? held-out retrieval evidence and train-only index metadata.
- `2_Dataset_Information/manifests/` ? frozen train/validation/test membership.
- `4_Final_Report/main.pdf` ? final Phase 1 report.

## Exclusions and limitations

The complete raw/processed COCO image collections are excluded. The 413 MB pairwise geometric-relationship detail CSV is excluded; its existing aggregate JSON summary and frequency CSV are included. The Python virtual environment, caches, temporary files, and inactive/obsolete LaTeX variants are excluded. Saved embeddings and FAISS indexes are included despite their size so the recorded retrieval artifacts can be reused. See `SUBMISSION_AUDIT.md` for detailed checks and hashes.

Phase 1 does not generate captions or compare RAG techniques. Historical EXIF/RGB conversion counts and a unified dependency lock are unavailable; exact caption mapping verification remains partial. The retrieval smoke test has 20 queries and no judged relevance labels.
