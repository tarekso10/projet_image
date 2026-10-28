# A Comparative Study of Dense Retrieval-Augmented Generation for Image Captioning

**Group:** [fill in] · **Members:** [fill in] · **Date:** [fill in]  
**Status:** Methods draft. Results are pending execution on the shared course split.

## Abstract

We compare a BLIP image-captioning baseline with a dense retrieval-augmented variant on a shared subset of MS COCO. The RAG system retrieves captions paired with visually similar training images using CLIP image embeddings and supplies those captions as generation context. We evaluate caption quality, retrieval performance, hallucinations, uncertainty, and computational cost. **Insert measured results only after running the frozen experiment.**

## 1. Introduction and problem statement

Image captioning systems can omit visible entities or generate unsupported details. Retrieval-augmented generation may ground a caption in examples from a separate image-caption collection. We ask whether dense image-to-image retrieval improves caption quality and visual grounding over the same captioner without retrieved context, and what retrieval and runtime costs it adds.

## 2. Related work

Discuss image captioning, CLIP-style image-text representation learning, retrieval-augmented generation, and hallucination evaluation. Cite primary papers and describe the exact model/checkpoint versions used. Do not rely on uncited generated summaries.

## 3. Assigned technique and hypotheses

The implemented method is naive dense RAG. CLIP embeds each knowledge-base image; the test image retrieves the top-k nearest training images by cosine similarity. Their five COCO training captions are candidate evidence. The five references for a test image are evaluation-only and never indexed. BLIP generates both baseline and evidence-conditioned captions using deterministic beam search.

H1: Dense RAG increases CIDEr relative to BLIP without retrieval. H2: Dense RAG lowers object, attribute, or relation hallucination rates. H3: Any quality gain increases latency and may not be statistically significant.

## 4. System architecture

COCO test image → CLIP image embedding → cosine nearest-neighbor search over training images → top-k associated training captions → BLIP generation → caption and metrics. The baseline omits retrieval evidence. Exact implementation and prompt are in `src/caption_rag/`.

## 5. Dataset and preprocessing

Report the exact COCO release, official/shared split source, train/validation/test counts, per-image caption counts, exclusions, image integrity audit, and split-file hashes. The assignment has a 100-versus-1,000 test-count discrepancy; state the instructor-approved resolution. Include the generated `dataset_summary.json`, object-class frequency, scene complexity, caption-length histogram, vocabulary size, and POS/diversity analyses. The local fallback split is not the course-wide stratified split.

## 6. Experimental protocol

| Setting | Value |
|---|---|
| Captioner | Salesforce/blip-image-captioning-base, [revision] |
| Image encoder | openai/clip-vit-base-patch32, [revision] |
| Knowledge base | 10,000 COCO train2017 images |
| Test set | [shared count and split ID hash] |
| Retrieval | cosine, exact dense search, top-k [selected on validation] |
| Generation | deterministic beam search, 3 beams, maximum 40 new tokens |
| Hardware/software | [GPU/CPU, RAM, Python, package versions] |

Include baseline versus RAG, tuning on validation only, retrieval Recall@k/Precision@k/MRR/latency, and at least the required ablations applicable to the assigned technique. The current code establishes baseline and RAG generation; add experiment records for tuning/ablations before treating this section as complete.

## 7. Results

### Caption quality

| Method | BLEU-4 | METEOR | ROUGE-L | CIDEr | SPICE | BERTScore |
|---|---:|---:|---:|---:|---:|---:|
| BLIP baseline | pending | pending | pending | pending | pending | pending |
| Dense RAG | pending | pending | pending | pending | pending | pending |

### Retrieval, latency, and uncertainty

Report Recall@1/5/10, Precision@k, MRR, retrieval latency, generation latency, confidence definition, ECE, and confidence-quality correlation. If a metric or confidence value was not measured, mark it unavailable and explain why.

## 8. Statistical tests

Compute per-image paired scores. Test normality of paired differences using Shapiro-Wilk. Use a paired t-test for normal differences or a Wilcoxon signed-rank test otherwise. Apply Bonferroni correction across the declared comparisons. Report corrected p-values, 95% confidence intervals, Cohen's dz or Rosenthal's r, and post-hoc power with the limitations of that calculation.

## 9. Hallucination analysis

Manually or with a validated annotation protocol assess a random 200-image sample. Define object, attribute, and relation errors before coding. Report annotator agreement and per-method rates with denominators and uncertainty intervals. COCO captions are not exhaustive scene annotations, so unsupported-by-reference does not by itself prove visual hallucination.

## 10. Ablation analysis

Report validation-selected top-k (1, 3, 5, 10), retrieval removal, encoder/model alternatives, and oracle-versus-actual retrieval where feasible. Clearly state which ablations were run and keep test data out of selection decisions.

## 11. Qualitative analysis

For successful and failed examples, include image ID, visual analysis, retrieved evidence with similarity scores, generated caption, reference captions, metric outcomes, and an explanation. Do not expose private/local absolute paths in the public report.

## 12. Discussion, limitations, and conclusion

Interpret measured results, including retrieval errors, evidence noise, caption-reference incompleteness, compute constraints, and the mismatch between lexical overlap metrics and grounded correctness. Avoid claiming that retrieval reduces hallucinations without the manual grounding analysis.

## Reproducibility appendix

Record install instructions, exact commands, package/model revisions, split hashes, random seed, index parameters and dimensions, data audit, and output filenames. Include repository URL and commit IDs after publication.
