# Paper Review Output Evaluation

Use this rubric for a completed matrix, comparison of two matrices, or explicit quality evaluation.
Score each dimension from 0 to 4; use `N/A` when the source does not permit assessment.

1. source and metadata verifiability;
2. extraction completeness;
3. provenance traceability;
4. factual and literal fidelity;
5. claim-evidence and modality fidelity;
6. deduplication and triage correctness;
7. cross-format export consistency;
8. user-request and column compliance.

Guardrail failures override aggregate scores. A fluent table with fabricated metadata or unsupported
findings is `FAIL`.

- **PASS**: no hard failures; all required dimensions are at least 3.
- **PASS_WITH_FLAGS**: no hard failures; only explicit unresolved source limitations remain.
- **FAIL**: fabricated content, missing required provenance, unverified rows presented as verified,
  or inconsistent master/export data.
