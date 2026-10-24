# Paper Review Output Guardrails

Run these checks after extraction and before displaying or exporting the review.

## Source and metadata integrity

- Every row has a verifiable DOI or a readable local file.
- DOI, title, authors, year, journal, publisher, URL, and document type match the source.
- Failed resolution is marked `UNVERIFIED`; never repair metadata from memory.
- Deduplication is based on DOI or normalized title and is recorded.

## Extraction and provenance integrity

- Every factual sentence in an extraction cell has `[AB]` or a section/paragraph marker such as `[M-2]`.
- Search-only records do not claim full-text methods, results, limitations, or future work unavailable in the abstract.
- Missing values use `—`; inferred summaries use `(summarized)` or an equivalent explicit flag.
- Findings, sample sizes, statistics, theories, gaps, and contributions preserve the paper's scope and modality.
- No invented paper, quote, result, method, DOI, page, quartile, or recommendation.

## Cross-format integrity

- `papers.json` is the single source of truth.
- Markdown, CSV/XLSX, BibTeX, XML, and RIS contain the same paper count and bibliographic values.
- Export transformations must not silently truncate provenance or alter literals.
- JSON and XML parse successfully; RIS has `TY` and `ER`; BibTeX has a valid entry key.

## Failure actions

| Failure | Action |
|---|---|
| Unsupported or fabricated content | Remove it or mark `—` / `UNVERIFIED`; do not deliver as fact. |
| Missing provenance | Re-extract from the source or flag the cell. |
| DOI/metadata mismatch | Preserve source data and mark `UNVERIFIED — check manually`. |
| Modality or scope drift | Rewrite conservatively and recheck against the paper. |
| Export mismatch | Regenerate every format from `papers.json`. |

`PASS_WITH_FLAGS` is allowed only for explicitly reported unresolved source limitations.
