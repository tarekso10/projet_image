# Phase 1 source code

This folder contains the original Python entry point, `src/` modules, configuration, and dependency declarations. No pipeline code or methodology was modified for this package.

## Install

Use Python 3.10 or newer in a clean environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Commands

`python main.py --help` lists the stages supported by the original CLI: `explore`, `select`, `preprocess`, `all`, `embeddings`, `text_embeddings`, `retrieval`, `caption_index`, `phash`, `pos`, `visual`, `quality`, `extended_analysis`, `metadata_redesign`, `replacement_plan`, `replacement_apply`, and `remaining`. Do not rerun selection or preprocessing against the completed frozen project.

Full pipeline execution requires MS COCO 2017 source images and annotations in paths configured by `configs/config.json`; those collections are intentionally not bundled. Model stages require their checkpoints to be locally available. Saved artifacts for this completed Phase 1 are in the sibling `2_Dataset_Information/` and `3_Results/` folders.
