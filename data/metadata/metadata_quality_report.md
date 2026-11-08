# Metadata Quality Report

Overall status: **PASS**

Validation applies to the existing root-level `train.json`, `validation.json`, and `test.json` image metadata files.

| Split | Images | Object annotations | Caption references |
|---|---:|---:|---:|
| train | 10000 | 134380 | 50000 |
| validation | 100 | 1022 | 500 |
| test | 1000 | 11715 | 5000 |

The validator checked JSON syntax, record consistency, frozen manifest order, source split, original filenames, object IDs and boxes, caption IDs, visual/geometric provenance, and protected artifact SHA-256 hashes.

COCO categories and boxes are ground-truth annotations. Color and edge values are image-processing calculations. Scene/context/time labels are CLIP predictions with relative uncalibrated softmax scores. Spatial counts are geometric inferences, not semantic ground truth.

Caption text remains in `data/captions/{split}.json`; image records contain IDs and a canonical file reference, not copies of caption text.

Protected artifact hashes unchanged: **PASS** (37 files).
Previous duplicate split-directory exports removed: `data/metadata/train`, `data/metadata/validation`, and `data/metadata/test`.
