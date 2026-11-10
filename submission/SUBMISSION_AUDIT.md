# Submission Audit

**Final readiness status: READY** ? the four submission categories are present, core checks passed, and evidence gaps are explicitly recorded below. This is package readiness; requirement-level project compliance remains **PARTIAL**.

## Submission structure

```text
submission/
??? README.md
??? 1_Source_Code/
??? 2_Dataset_Information/
??? 3_Results/
??? 4_Final_Report/
??? SUBMISSION_AUDIT.md
```

Files before adding this audit: 135; payload size before audit: 330,001,073 bytes. Counts by category: `1_Source_Code`: 16, `2_Dataset_Information`: 34, `3_Results`: 59, `4_Final_Report`: 25, `README.md`: 1.

### Files included

**1_Source_Code/**
- `1_Source_Code/README.md`
- `1_Source_Code/configs/config.json`
- `1_Source_Code/main.py`
- `1_Source_Code/requirements.txt`
- `1_Source_Code/src/__init__.py`
- `1_Source_Code/src/caption_pos.py`
- `1_Source_Code/src/controlled_replacement.py`
- `1_Source_Code/src/embeddings.py`
- `1_Source_Code/src/extended_analysis.py`
- `1_Source_Code/src/metadata_redesign.py`
- `1_Source_Code/src/perceptual_hash.py`
- `1_Source_Code/src/pipeline.py`
- `1_Source_Code/src/quality_control.py`
- `1_Source_Code/src/retrieval.py`
- `1_Source_Code/src/text_embeddings.py`
- `1_Source_Code/src/visual_analysis.py`

**2_Dataset_Information/**
- `2_Dataset_Information/dataset_description.md`
- `2_Dataset_Information/dataset_statistics/caption_length_distribution.csv`
- `2_Dataset_Information/dataset_statistics/caption_token_counts.csv`
- `2_Dataset_Information/dataset_statistics/caption_vocabulary_statistics.json`
- `2_Dataset_Information/dataset_statistics/caption_word_frequencies.csv`
- `2_Dataset_Information/dataset_statistics/caption_word_frequencies_top500.csv`
- `2_Dataset_Information/dataset_statistics/dataset_audit.json`
- `2_Dataset_Information/dataset_statistics/geometric_spatial_relationship_frequencies.csv`
- `2_Dataset_Information/dataset_statistics/geometric_spatial_relationships_summary.json`
- `2_Dataset_Information/dataset_statistics/train2017_category_frequencies.csv`
- `2_Dataset_Information/dataset_statistics/train2017_dimensions.csv`
- `2_Dataset_Information/dataset_statistics/train2017_object_count_distribution.csv`
- `2_Dataset_Information/dataset_statistics/train_val_category_cooccurrence.csv`
- `2_Dataset_Information/dataset_statistics/val2017_category_frequencies.csv`
- `2_Dataset_Information/dataset_statistics/val2017_dimensions.csv`
- `2_Dataset_Information/dataset_statistics/val2017_object_count_distribution.csv`
- `2_Dataset_Information/manifests/revision_1.json`
- `2_Dataset_Information/manifests/test_ids.csv`
- `2_Dataset_Information/manifests/test_ids.json`
- `2_Dataset_Information/manifests/train_ids.csv`
- `2_Dataset_Information/manifests/train_ids.json`
- `2_Dataset_Information/manifests/validation_ids.csv`
- `2_Dataset_Information/manifests/validation_ids.json`
- `2_Dataset_Information/metadata/color_shape_diversity.csv`
- `2_Dataset_Information/metadata/color_shape_diversity.json`
- `2_Dataset_Information/metadata/metadata_schema.json`
- `2_Dataset_Information/metadata/spatial_relationships_per_image.json`
- `2_Dataset_Information/metadata/test.json`
- `2_Dataset_Information/metadata/train.json`
- `2_Dataset_Information/metadata/validation.json`
- `2_Dataset_Information/reference_captions/test.json`
- `2_Dataset_Information/reference_captions/train.json`
- `2_Dataset_Information/reference_captions/validation.json`
- `2_Dataset_Information/selection_report.json`

**3_Results/**
- `3_Results/.gitattributes`
- `3_Results/FINAL_SCIENTIFIC_AUDIT.md`
- `3_Results/embeddings/image_embeddings/extraction_statistics.json`
- `3_Results/embeddings/image_embeddings/test.done.npy`
- `3_Results/embeddings/image_embeddings/test.metadata.json`
- `3_Results/embeddings/image_embeddings/test.npy`
- `3_Results/embeddings/image_embeddings/test.run.json`
- `3_Results/embeddings/image_embeddings/train.done.npy`
- `3_Results/embeddings/image_embeddings/train.metadata.json`
- `3_Results/embeddings/image_embeddings/train.npy`
- `3_Results/embeddings/image_embeddings/train.run.json`
- `3_Results/embeddings/image_embeddings/validation.done.npy`
- `3_Results/embeddings/image_embeddings/validation.metadata.json`
- `3_Results/embeddings/image_embeddings/validation.npy`
- `3_Results/embeddings/image_embeddings/validation.run.json`
- `3_Results/embeddings/text_embeddings/extraction_statistics.json`
- `3_Results/embeddings/text_embeddings/train.done.npy`
- `3_Results/embeddings/text_embeddings/train.metadata.json`
- `3_Results/embeddings/text_embeddings/train.npy`
- `3_Results/exploration/README.md`
- `3_Results/exploration/extended_analysis_run.json`
- `3_Results/exploration/figures/caption_length_distribution.png`
- `3_Results/exploration/figures/caption_pos_distribution.png`
- `3_Results/exploration/figures/caption_vocabulary_rank_frequency.png`
- `3_Results/exploration/figures/caption_vocabulary_top30.png`
- `3_Results/exploration/figures/caption_word_frequencies.png`
- `3_Results/exploration/figures/color_family_distribution.png`
- `3_Results/exploration/figures/geometric_relationship_frequencies.png`
- `3_Results/exploration/figures/image_edge_density_distribution.png`
- `3_Results/exploration/figures/object_cooccurrence_matrix.png`
- `3_Results/exploration/figures/selected_scene_complexity.png`
- `3_Results/exploration/figures/test_category_distribution.png`
- `3_Results/exploration/figures/top50_object_classes.png`
- `3_Results/preprocessing/frozen_manifest_resume_check.json`
- `3_Results/preprocessing/preprocessing.json`
- `3_Results/preprocessing/selected_images_integrity.json`
- `3_Results/preprocessing/validation_preprocessing_comparison.csv`
- `3_Results/preprocessing/validation_preprocessing_comparison.json`
- `3_Results/preprocessing/validation_preprocessing_comparison.png`
- `3_Results/quality_control/PHASE1_FINAL_COMPLIANCE_REPORT.md`
- `3_Results/quality_control/cleanup_report.json`
- `3_Results/quality_control/cross_split_pair_evidence.json`
- `3_Results/quality_control/cross_split_visual_review.json`
- `3_Results/quality_control/final_quality_control.json`
- `3_Results/quality_control/hash_statistics.json`
- `3_Results/quality_control/phase1_final_compliance.json`
- `3_Results/quality_control/phash_database.npz`
- `3_Results/quality_control/pos_distribution.csv`
- `3_Results/quality_control/pos_linguistic_summary.json`
- `3_Results/quality_control/uncertain_predictions.json`
- `3_Results/quality_control/visual_analysis_summary.json`
- `3_Results/retrieval/caption_index_statistics.json`
- `3_Results/retrieval/faiss_indexes/caption_text_cosine_train.index`
- `3_Results/retrieval/faiss_indexes/caption_text_cosine_train.metadata.json`
- `3_Results/retrieval/faiss_indexes/image_cosine_train.index`
- `3_Results/retrieval/faiss_indexes/image_cosine_train.metadata.json`
- `3_Results/retrieval/heldout_image_similarity.json`
- `3_Results/retrieval/retrieval_evaluation.json`
- `3_Results/retrieval/retrieval_stage.json`

**4_Final_Report/**
- `4_Final_Report/LaTeX_Source/README.md`
- `4_Final_Report/LaTeX_Source/figures/caption_length_distribution.png`
- `4_Final_Report/LaTeX_Source/figures/caption_pos_distribution.png`
- `4_Final_Report/LaTeX_Source/figures/color_family_distribution.png`
- `4_Final_Report/LaTeX_Source/figures/preprocessing_geometry_summary.png`
- `4_Final_Report/LaTeX_Source/figures/top50_object_classes.png`
- `4_Final_Report/LaTeX_Source/main.tex`
- `4_Final_Report/LaTeX_Source/references.bib`
- `4_Final_Report/LaTeX_Source/sections/appendix_artifacts_new.tex`
- `4_Final_Report/LaTeX_Source/sections/chapter1_introduction.tex`
- `4_Final_Report/LaTeX_Source/sections/chapter2_dataset.tex`
- `4_Final_Report/LaTeX_Source/sections/chapter3_exploration.tex`
- `4_Final_Report/LaTeX_Source/sections/embeddings.tex`
- `4_Final_Report/LaTeX_Source/sections/knowledge_base.tex`
- `4_Final_Report/LaTeX_Source/sections/limitations.tex`
- `4_Final_Report/LaTeX_Source/sections/metadata.tex`
- `4_Final_Report/LaTeX_Source/sections/phase2_plan.tex`
- `4_Final_Report/LaTeX_Source/sections/preprocessing.tex`
- `4_Final_Report/LaTeX_Source/sections/results_discussion.tex`
- `4_Final_Report/LaTeX_Source/sections/retrieval.tex`
- `4_Final_Report/LaTeX_Source/tables/config_summary.tex`
- `4_Final_Report/LaTeX_Source/tables/dataset_summary.tex`
- `4_Final_Report/LaTeX_Source/tables/index_summary.tex`
- `4_Final_Report/LaTeX_Source/tables/qc_summary.tex`
- `4_Final_Report/main.pdf`

## Files intentionally excluded

- Original COCO `train2017`/`val2017` images, processed image trees, and full COCO annotation dumps: excluded as instructed; obtain MS COCO 2017 separately to rerun image processing.
- `reports/statistical_analysis/geometric_spatial_relationships.csv` (413,097,783 bytes): pairwise detail table excluded for size; its aggregate JSON and frequency CSV are included.
- Local `venv/`, `.git/`, caches, temporary build files, inactive LaTeX variants, and the 15 MB `project_structure.txt` are not needed.
- Four small PNGs are present both under Results and the LaTeX source bundle to keep the report source self-contained. This duplication is intentional and byte-identical.
- `report_phase1.pdf` is an older build with identical extracted text. The later `reports/final_report/main.pdf` is used. The legacy root `report.pdf` is absent from the working tree; it was not restored or overwritten.

## Missing or unavailable files

- The full per-image `data/metadata/visual_predictions.jsonl` and its sidecar are absent. The available aggregate visual-analysis summary and uncertain-prediction records are included; detailed predictions cannot be reconstructed from these summaries.
- `data/metadata/metadata_quality_report.json` and `.md` are absent from the workspace and are not fabricated. Available per-split metadata, schema, dataset audit, QC, and compliance evidence are included.
- A unified dependency lock and historical EXIF/RGB conversion counts are unavailable, as documented by the project.
- No required top-level submission category is missing. Original COCO data are intentionally excluded, not missing deliverables.

## Verification results

- Required source, dataset, results, and final-report folders and key files exist.
- `python main.py --help` ran from packaged `1_Source_Code/` and listed the documented CLI commands. The project environment passed `pip check`; required packages imported and spaCy `en_core_web_sm` 3.8.0 was present. No virtual environment was copied.
- Frozen manifests contain 10,000/100/1,000 unique IDs with no pairwise overlap. Selected caption exports contain 50,000/500/5,000 records, exactly five captions for every manifest image.
- Saved vectors load as finite float32 arrays with dimension 512 and unit L2 norms: image train/validation/test = 10,000/100/1,000; training captions = 50,000. FAISS readback succeeded: image 10,000 x 512, captions 50,000 x 512. Caption-index metadata says no validation/test captions are included.
- Saved pipeline QC is **PASS**. Separate requirement-level compliance is **PARTIAL**. Saved retrieval evidence records 20 held-out queries, zero self-matches, and mean top-1 cosine 0.8260.
- PDF opens, is unencrypted, and has 15 pages. Extracted text confirms 10,000 train, 100 validation, 1,000 test, PARTIAL status, and 0.8260. No obsolete claim that the assignment PDF was unavailable is present; the report notes the `1,00` typo and resolves the intended size to 1,000.
- `reports/final_report/main.pdf` is the latest PDF found (10 Nov 2026 21:56 local; alternate PDF 18:45). PDF author metadata matches the four students on its title page.
- All LaTeX inputs, nested table inputs, and five graphics resolve. The 23 non-README entries in the existing `overleaf_upload.zip` match the packaged LaTeX sources/assets by SHA-256. No Tectonic/LaTeX executable is installed, so the source was not recompiled; the included existing PDF was checked directly.
- SHA-256 matched original copies for the final PDF, three manifests, four embedding arrays, two FAISS indexes, and QC/compliance JSON files.
- `3_Results/.gitattributes` configures the two result files over 100 MB for Git LFS; their local payloads remain unchanged. The LFS pointers keep the GitHub commit below its per-file hard limit.

### SHA-256 evidence

| Artifact | SHA-256 |
|---|---|
| Final PDF | `fe61174410385c9fab41387690ba3bf5c928983bf5231db7648885e25f24719c` |
| Train manifest | `eee87e12ff6c89a33035bcc2daf43e9433210079226d68d1ec44087688e34f3e` |
| Validation manifest | `1fa9a5d8ec55b7aca28d5c1faba9fc192527bf26df3601887fd09c3a01ca1537` |
| Test manifest | `15bdf3dc09a74e7d5dfcd2805209f38dd4a3c4cbde147293926902d7f013d304` |
| Image train embeddings | `2f79da597521b20389c48f4916a2a22af3fe7a94b8591d5a842afb153822143e` |
| Image validation embeddings | `9cbe6d304cf6186e1128a83bb0517fc598d3f31e91a3ac85b590d671e656af0b` |
| Image test embeddings | `8a2f952904596e97e3a6b4906b4e17547ee85521041f13d44278c269608a7fb8` |
| Text train embeddings | `105c6ba9f5ecdb6ca1b20bd52e98528bc194d3da29a1c4f9f9c1c38a9255934b` |
| Image FAISS index | `8a01188834a28f47a4bdd670e830246c0cdea227cf48efdf960cdb64a9385f29` |
| Caption FAISS index | `4490061264023e798ff6b1bc110d623f96dfc2d3db9e986301deed211a86bde8` |
| Pipeline QC JSON | `80774c56105b6a0506f3dbbbfe8feaee81bb895cced923679bcdc350532f56f6` |
| Compliance audit JSON | `b7d5a5ef82e4176658d86bd0f96c25563d38d46970e7820a8a8763432e42fc1e` |

- No raw COCO `.jpg`/`.jpeg`/`.webp` images, `.git`, `venv`, `.venv`, or `__pycache__` are in the package.

## Remaining limitations

- Phase 1 does not generate captions or compare RAG techniques.
- Full pipeline reruns require original COCO assets and local model checkpoints, which are not bundled.
- Detailed per-image CLIP predictions and the metadata-specific quality report are unavailable in this workspace.
- Requirement-level compliance remains **PARTIAL**, including partial exact caption-mapping verification and incomplete environment/preprocessing history.

## Final readiness

**READY** as a Phase 1 package: all four requested categories contain available evidence, report/source are included, key artifacts were checked, and omissions and scientific limitations are disclosed. READY describes packaging only; project compliance remains **PARTIAL**.
