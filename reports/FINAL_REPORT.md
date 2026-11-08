# Final Phase 1 quality report

Overall status: **PASS**; Phase 1 complete: **True**.

## Dataset and frozen splits

- Split counts: train 10,000, validation 100, test 1,000.
- Candidate exclusions for non-five caption cardinality: train 315; val 13. Frozen manifests were not modified by remaining stages.
- COCO train2017 annotations: 118,287 images, 860,001 object instances, 591,753 captions.
- COCO val2017 annotations: 5,000 images, 36,781 object instances, 25,014 captions.

## Embeddings and retrieval

- Image encoder: openai/clip-vit-base-patch32 (revision 3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268); device cpu; dimension 512; elapsed 2.07 s.
- Image vectors: train 10,000, validation 100, test 1,000; float32, L2-normalized, finite; ID order checked against frozen manifests.
- Image FAISS index: 10000 train vectors, 20480045 bytes, build 0.158 s.
- Image retrieval: 20 held-out queries, top-5, self matches 0, mean top-1 cosine 0.8260029643774033.
- Caption vectors: 50000 train captions, 512 dimensions, model revision 3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268, elapsed 1121.3 s.
- Caption FAISS index: 50000 train-only vectors, 102400045 bytes, build 0.868 s; held-out caption IDs in KB: 0.

## Perceptual duplicate audit

- DCT pHash: 11100 images; inclusive Hamming threshold 6; 9 review candidates, including 0 across splits.
- Candidate distances: {'0': 1, '2': 2, '4': 2, '6': 4}. Exact SHA-256 audit found 0 exact duplicate groups.
- Original-resolution review of all four train/test candidates:
- Final audit decision: **PASS**. The historical d=2 pair had strong visual near-duplicate evidence but no provenance metadata establishing whether it was the same source capture. Both IDs were removed from the current train/test combination through controlled test replacement. Current pHash found no cross-split candidates at inclusive Hamming threshold 6.
- Pair-level evidence and original-resolution visual comparisons are in `reports/perceptual_hash/cross_split_pair_evidence.json`, `cross_split_native_resolution_comparison.png`, and `hamming2_native_2x.png`. No source result files or manifests were changed.

## POS and visual analysis

- spaCy POS: model en_core_web_sm; 55500 captions; 642147 tokens; errors 0.
- Most frequent nouns: [['man', 6754], ['people', 5494], ['table', 5467], ['kitchen', 4091], ['woman', 3860], ['street', 3800], ['food', 2945], ['plate', 2876], ['room', 2819], ['computer', 2396]].
- Most frequent verbs: [['sit', 6401], ['stand', 4212], ['hold', 2437], ['walk', 1915], ['have', 1775], ['eat', 1496], ['play', 1415], ['rid', 1299], ['look', 1294], ['be', 1172]].
- Most frequent adjectives: [['white', 2897], ['large', 2271], ['small', 1843], ['black', 1625], ['young', 1296], ['other', 1167], ['red', 1018], ['several', 995], ['wooden', 956], ['many', 893]].
- CLIP scene/context predictions: 11100 images; uncertain context/time/scene counts {'context': 197, 'time': 582, 'scene': 1063}; confidence summary {'indoor_outdoor': {'mean_score': 0.9281779026555586, 'mean_accepted_score': 0.9354509744285104, 'min_score': 0.500175952911377}, 'day_night': {'mean_score': 0.8387563212551512, 'mean_accepted_score': 0.8561028413705487, 'min_score': 0.5000872611999512}, 'scene': {'mean_score': 0.650040950470411, 'mean_accepted_score': 0.6876669611851984, 'min_score': 0.1633705496788025}}.
- Scene labels are zero-shot model predictions with uncalibrated softmax scores; low-confidence output is UNKNOWN. COCO categories remain separate annotations. Color is a coarse pixel-level hue/luminance proxy.

## Check results

- **PASS** `count_train`: {"expected": 10000, "actual": 10000}
- **PASS** `five_captions_train`: {"images_with_wrong_caption_count": {}, "caption_records": 50000}
- **PASS** `processed_files_train`: {"missing_count": 0, "examples": []}
- **PASS** `decode_train`: {"decoded": 10000, "errors": []}
- **PASS** `count_validation`: {"expected": 100, "actual": 100}
- **PASS** `five_captions_validation`: {"images_with_wrong_caption_count": {}, "caption_records": 500}
- **PASS** `processed_files_validation`: {"missing_count": 0, "examples": []}
- **PASS** `decode_validation`: {"decoded": 100, "errors": []}
- **PASS** `count_test`: {"expected": 1000, "actual": 1000}
- **PASS** `five_captions_test`: {"images_with_wrong_caption_count": {}, "caption_records": 5000}
- **PASS** `processed_files_test`: {"missing_count": 0, "examples": []}
- **PASS** `decode_test`: {"decoded": 1000, "errors": []}
- **PASS** `overlap_train_validation`: {"count": 0, "examples": []}
- **PASS** `overlap_train_test`: {"count": 0, "examples": []}
- **PASS** `overlap_validation_test`: {"count": 0, "examples": []}
- **PASS** `exact_sha256`: {"duplicate_groups": 0}
- **PASS** `perceptual_hash`: {"images_hashed": 11100, "candidate_pairs": 9, "threshold": 6, "cross_split_candidates": 0, "cross_split_pairs_reviewed": 0, "review_classifications": {}, "unresolved_pairs": [], "manual_review_report_present": true, "errors": 0}
- **PASS** `historical_sha256_and_phash_results_archived`: {"artifacts_checked": 4, "all_archived_byte_for_byte": true, "current_revision_recomputed": true}
- **PASS** `image_embeddings`: {"train": {"shape": [10000, 512], "finite": true, "unit_norm": true}, "validation": {"shape": [100, 512], "finite": true, "unit_norm": true}, "test": {"shape": [1000, 512], "finite": true, "unit_norm": true}}
- **PASS** `embedding_id_mapping`: {"train": {"rows": 10000, "matches_manifest_order": true}, "validation": {"rows": 100, "matches_manifest_order": true}, "test": {"rows": 1000, "matches_manifest_order": true}}
- **PASS** `faiss_index`: {"ntotal": 10000, "dimension": 512, "index_type": "IndexFlatIP"}
- **PASS** `retrieval`: {"status": "PASS", "query_count": 20, "requested_query_count": 20, "top_k": 5, "successful_queries": 20, "queries_without_results": [], "gallery_count": 10000, "gallery_split": "train", "query_splits": ["validation", "test"], "self_match_count": 0, "mean_top1_cosine": 0.8260029643774033, "index_readback_valid": true}
- **PASS** `caption_text_embeddings_and_caption_vector_database`: {"shape": [50000, 512], "mapping_matches_source": true, "unique_train_caption_ids": 50000, "heldout_caption_ids_in_index": 0, "faiss_count": 50000}
- **PASS** `pos_tagging`: {"caption_counts": {"train": {"records": 50000, "malformed": []}, "validation": {"records": 500, "malformed": []}, "test": {"records": 5000, "malformed": []}}, "expected": {"train": 50000, "validation": 500, "test": 5000}}
- **PASS** `visual_analysis`: {"records": 11100, "expected": 11100, "malformed_records": 0}
- **PASS** `frozen_manifest_consistency`: {"matches_selection_report": {"train": true, "validation": true, "test": true}, "configured_seed": 20261106}
- **PASS** `controlled_manifest_revision_integrity`: {"backup_files": 15, "originals_match_backup": true, "train_validation_unchanged": true, "current_hashes_match_revision_record": true, "test_manifest_intentionally_revised": true}

## Items requiring attention

NOT_RUN checks: none.
WARNING checks: none.
FAIL checks: none.
A full-completion claim requires every applicable check to be PASS. Visual model scores are not calibrated probabilities, and perceptual-hash candidates are not confirmed duplicates. COCO provides no explicit relation labels; no interaction claims are made.
