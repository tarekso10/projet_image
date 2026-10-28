"""Caption metrics and paired statistical comparisons."""

from __future__ import annotations

import numpy as np
from scipy import stats


def paired_comparison(a: list[float], b: list[float], comparisons: int = 1) -> dict:
    """Compare paired per-image scores; choose paired t-test or Wilcoxon by Shapiro test."""
    if len(a) != len(b) or len(a) < 3:
        raise ValueError("paired samples must have the same length and at least three observations")
    x, y = np.asarray(a, float), np.asarray(b, float)
    delta = y - x
    shapiro_p = float(stats.shapiro(delta).pvalue)
    if shapiro_p >= 0.05:
        test = stats.ttest_rel(y, x)
        sd = float(np.std(delta, ddof=1))
        effect = float(np.mean(delta) / sd) if sd else 0.0
        effect_name = "cohen_dz"
        test_name = "paired_t"
    else:
        test = stats.wilcoxon(y, x, zero_method="wilcox", alternative="two-sided", method="auto")
        n_eff = max(1, int(np.count_nonzero(delta)))
        # Signed-rank z approximation; report this as an approximate effect size.
        z = float(stats.norm.isf(float(test.pvalue) / 2) * np.sign(np.median(delta)))
        effect = z / np.sqrt(n_eff)
        effect_name = "rosenthal_r_approx"
        test_name = "wilcoxon_signed_rank"
    p = float(test.pvalue)
    return {"test": test_name, "shapiro_p": shapiro_p, "p_value": p,
            "p_bonferroni": min(1.0, p * comparisons),
            "alpha_bonferroni": 0.05 / comparisons,
            "effect_name": effect_name, "effect_size": effect,
            "mean_difference": float(np.mean(delta)),
            "ci95_low": float(np.mean(delta) - 1.96 * stats.sem(delta)),
            "ci95_high": float(np.mean(delta) + 1.96 * stats.sem(delta))}


def caption_metrics(predictions: list[str], references: list[list[str]]) -> dict[str, float]:
    """Use COCO caption evaluator when installed; never silently fabricate a metric."""
    try:
        from pycocoevalcap.bleu.bleu import Bleu
        from pycocoevalcap.cider.cider import Cider
        from pycocoevalcap.meteor.meteor import Meteor
        from pycocoevalcap.rouge.rouge import Rouge
        from pycocoevalcap.spice.spice import Spice
    except ImportError as exc:
        raise RuntimeError('Install COCO metric dependencies with: pip install -e ".[metrics]"') from exc
    gts = {i: refs for i, refs in enumerate(references)}
    res = {i: [pred] for i, pred in enumerate(predictions)}
    out: dict[str, float] = {}
    for name, evaluator in (("bleu", Bleu(4)), ("meteor", Meteor()), ("rouge", Rouge()),
                            ("cider", Cider()), ("spice", Spice())):
        score, _ = evaluator.compute_score(gts, res)
        if name == "bleu":
            out.update({f"bleu_{i+1}": float(score[i]) for i in range(4)})
        else:
            out[name] = float(score)
    return out


def caption_metrics_per_image(predictions: list[str], references: list[list[str]]) -> dict[str, list[float]]:
    """Return per-image scores required for paired inference, alongside aggregate scores."""
    try:
        from pycocoevalcap.bleu.bleu import Bleu
        from pycocoevalcap.cider.cider import Cider
        from pycocoevalcap.meteor.meteor import Meteor
        from pycocoevalcap.rouge.rouge import Rouge
        from pycocoevalcap.spice.spice import Spice
    except ImportError as exc:
        raise RuntimeError('Install COCO metric dependencies with: pip install -e ".[metrics]"') from exc
    gts = {i: refs for i, refs in enumerate(references)}
    res = {i: [pred] for i, pred in enumerate(predictions)}
    out: dict[str, list[float]] = {}
    for name, evaluator in (("bleu", Bleu(4)), ("meteor", Meteor()), ("rouge", Rouge()),
                            ("cider", Cider()), ("spice", Spice())):
        _, per_item = evaluator.compute_score(gts, res)
        if name == "bleu":
            for i in range(4):
                out[f"bleu_{i+1}"] = [float(x) for x in per_item[i]]
        else:
            out[name] = [float(x) for x in per_item]
    return out
