# LLM Eval-Driven Development (EDD), DeepEval, LLM-as-a-Judge & GraphRAG Evals

Authoritative guide for engineering deterministic evaluation gates, calibrated LLM-as-a-Judge pipelines, GraphRAG multi-hop evaluation, and closed-loop production drift monitoring.

---

## 1. Eval-Driven Development (EDD) & Stratified Golden Datasets

Treat prompts, retrieval settings, and routing policies like code under **Eval-Driven Development**:
- **Stratified Golden Dataset**: Maintain 150–200 versioned test cases spanning core happy-path queries, adversarial edge cases, and historical production regressions.
- **CI Merge Gates**: Every pull request touching prompts, chunking logic, or model configs executes offline evaluation (`deepeval test run`) and blocks merge if faithfulness, precision, or safety drops below threshold.

```python
from __future__ import annotations

from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

def test_rag_faithfulness_gate() -> None:
    """Unit-tests RAG faithfulness inside standard pytest CI pipelines."""
    test_case = LLMTestCase(
        input="What is the max connection pool formula?",
        actual_output="MaxConnections = N_pods * N_workers * (PoolSize + MaxOverflow) <= 0.80 * C_PgBouncerMax.",
        retrieval_context=[
            "MaxConnections = N_pods * N_workers * (PoolSize + MaxOverflow) <= 0.80 * C_PgBouncerMax."
        ],
    )
    faithfulness = FaithfulnessMetric(threshold=0.85, include_reason=True)
    relevancy = AnswerRelevancyMetric(threshold=0.80)
    assert_test(test_case, [faithfulness, relevancy])
```

---

## 2. LLM-as-a-Judge Calibration & Bias Mitigation

Naive LLM judges suffer from **verbosity bias**, **position bias**, and **self-model preference**. Enforce strict judge engineering:
1. **G-Eval Rubric Deconstruction**: Score explicit sub-criteria step-by-step with Chain-of-Thought reasoning rather than coarse 1–5 holistic scores.
2. **Deterministic Screening Tiers**: Run cheap AST, regex, JSON Schema, and embedding checks first; invoke frontier LLM judges only on nuanced semantic criteria.
3. **Cross-Family Judging & Position Swapping**: Never judge a model's output with the same model family; swap candidate order `(A, B)` and `(B, A)` during pairwise comparisons.
4. **Human Calibration Gate**: Track Cohen's kappa agreement between automated judges and human SME labels; require `kappa >= 0.85` before trusting automated CI blocks.

---

## 3. GraphRAG Multi-Hop Evals & Closed-Loop Production Sampling

- **GraphRAG Evaluation**: Beyond flat chunk precision/recall, score *entity-link traversal completeness* (multi-hop edge coverage) and *community summary faithfulness* (ensuring synthesis across clusters does not fabricate relations).
- **Closed-Loop Trace Sampling**: Asynchronously sample `5%–20%` of live production traffic through the identical offline eval suite, automatically promoting clustered production failures into the versioned Golden Dataset.
