# Final academic report

The LaTeX source and generated project figures are in this directory. The main document is `main.tex`; references are in `references.bib`.

## Compile

From this directory, run:

```powershell
tectonic main.tex
```

Tectonic was used to compile the delivered PDF. If using a traditional TeX distribution instead, run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. The expected output is `main.pdf`.

## Evidence and scope

The report is grounded in the current source, manifests, generated reports, and visualizations in the parent project. It describes completed data preparation and retrieval only. Caption generation, comparative RAG evaluation, caption-quality metrics, statistical testing, ablation, and hallucination analysis are explicitly marked pending. The original assignment PDF was not found in the audited project locations; the 100-versus-1,000 test discrepancy is reported from the supplied project specification.

Most figures were copied from the existing `visualizations/` directory. The preprocessing summary chart was newly plotted from the recorded validation comparison JSON. No experimental outcomes were fabricated. Rebuild the document after editing the `.tex` or bibliography files.
