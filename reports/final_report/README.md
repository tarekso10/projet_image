# Phase 1 Final Report

This directory contains the concise 15-page LaTeX report **A Comparative Study of RAG Techniques for Generating Image Captions — Phase 1: Dataset Exploration and Preprocessing**. Its structure is: Introduction and Objectives; Dataset and Splitting; Data Exploration; Preprocessing; Metadata; Embeddings; Knowledge Base and FAISS; Retrieval and Quality Control; Results and Discussion; and Limitations and Conclusion. An appendix summarizes reproducibility settings.

## Compile

From this directory, build the PDF with either:

```powershell
tectonic main.tex
```

or

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The output is `main.pdf`. The report was validated using Tectonic 0.17.0. Compilation does not run or modify the dataset and model pipeline.

## Contents

- `main.tex` — layout, cover, abstract, contents, and included sections.
- `sections/` — the active report content.
- `tables/` — dataset, index, configuration, and quality-control summaries.
- `figures/` — report figures; a few referenced charts are read from `../../visualizations/`.
- `references.bib` — cited papers and official documentation.

## Evidence scope

The report uses saved project evidence. The pipeline quality-control checks pass, but the separate assignment-compliance audit remains **PARTIAL**. Caption generation, RAG comparisons, caption metrics, hallucination analysis, statistical comparisons, and ablations have not been completed.
