---
name: paper-review
description: Builds a verifiable literature-review synthesis matrix from online searches, local PDF or LaTeX files, or both, producing per-paper Markdown tables and optional CSV, XLSX, BibTeX, EndNote XML, and RIS exports. Use when creating a literature review matrix, extracting structured paper tables (purpose, method, findings, limitations, gaps, theory, novelty, future work, DOI), synthesizing academic papers, or exporting verified bibliography records.
---

# Paper Review

This skill builds a structured literature-review and data-extraction matrix. It supports Search,
Folder, and Hybrid input modes. All instructions in this file and its referenced modules are in
English. Follow the user's requested output language for extracted content.

## Usage

The skill activates automatically for literature-matrix, paper-review, paper-synthesis, PDF/LaTeX
extraction, and bibliography-export requests. Users may also invoke it explicitly by name:

```text
Use paper-review in Search mode. Review 15 papers on [topic], preserve provenance,
verify DOI metadata, build papers.json, and validate before exporting.
```

Select `Search`, `Folder`, or `Hybrid` from the request. If the mode, scope, columns, filters, or
export formats are ambiguous, ask once before acquisition. Do not require a slash command when the
host supports natural-language skill activation.

## Mandatory load order

1. Load this `SKILL.md`.
2. Load `references/search-sources.md` for online acquisition, or
   `references/extracting-papers.md` for local PDF/LaTeX extraction.
3. Load `references/table-builder.md` before rendering or exporting.
4. Load `protocols/output-guardrails.md` before delivery.
5. For substantial matrices or comparisons, load `protocols/evaluation.md` and
   `references/output-rubric.md`.

## Input modes

| Mode | Use when | Sources |
|---|---|---|
| **Search** | The user provides a topic, keywords, and optional target count | OpenAlex, Semantic Scholar, arXiv, Crossref, DOI, publishers, and web tools |
| **Folder** | The user provides a folder of papers | Local PDF or LaTeX files |
| **Hybrid** | The user requests both | Merge search and local results, then deduplicate |

## Pipeline & workflow checklist

Copy this checklist and track progress internally before delivering:

- [ ] **Step 0 — Clarify**: Confirm input mode (`Search`, `Folder`, or `Hybrid`), topic/keywords, target count, columns, filters (years, quartile), language, and export formats.
- [ ] **Step 1 — Acquire & verify**: Collect, deduplicate, and verify papers (`references/search-sources.md` or `references/extracting-papers.md`).
- [ ] **Step 2 — Extract with provenance**: Read available sources and populate every agreed field with `[AB]` or section markers (`[I-1]`, `[M-2]`, `[R-1]`, etc.).
- [ ] **Step 3 — Build & export**: Create `papers.json` as the master source, render `literature_table.md`, and run `scripts/export_formats.py` for requested formats (`references/table-builder.md`).
- [ ] **Step 4 — Validate**: Run `protocols/output-guardrails.md`, DOI checks, and quality gates (`protocols/evaluation.md` + `references/output-rubric.md`) before delivering.

Ask for one initial confirmation when the scope is unclear. Do not ask for confirmation for each
candidate after the user has approved the topic, count, columns, and filters.

## Step 0 — Clarify

Confirm only the parameters that are not already clear:

- input mode: Search, Folder, or Hybrid;
- topic, keywords, and target number;
- default or custom columns;
- meaning of `Gaps`: gap addressed by the paper or potential new research gap;
- publication-year range and document type;
- journal-quality filter: Q1/Q2/Q3/Q4, peer-reviewed only, or no filter;
- paper language and output language;
- Markdown and requested export formats;
- local folder path for Folder or Hybrid mode.

Default to 10–15 papers for Search, all eligible files for Folder, the default matrix columns, the
last five years, English papers, and Markdown output unless the user specifies otherwise.

## Step 1 — Acquire and verify

### Search mode

1. Decompose the topic into 3–5 concepts and create 8–15 query combinations.
2. Search OpenAlex first, then use Semantic Scholar, arXiv, Crossref, publishers, or web tools as needed.
3. Collect approximately 1.5 times the target count as candidates.
4. Score title/abstract relevance from 0–10 and retain candidates scoring at least 7 until the target is met.
5. Record DOI, title, abstract, authors, year, journal, publisher, URL, query, source, and search date.

### Folder mode

1. Recursively scan the target folder for `.pdf` and `.tex` files.
2. Read LaTeX directly. Extract PDF text with `scripts/extract_text.sh`, `pdftotext`, or an available PDF library.
3. Read the abstract, introduction, methods, results, discussion, limitations, conclusion, and future-work sections as available.
4. If extraction is incomplete, use only the readable content and mark unavailable fields `—`.

### Hybrid mode

Merge search and local results. Prefer local full text over search metadata. Deduplicate by DOI; if
no DOI exists, use a normalized title. Keep a record of removed duplicates.

### Verification rules

- Every row must have a verifiable DOI or a readable local file.
- Resolve each DOI when web access is available.
- Mark failed resolution `UNVERIFIED — check manually`.
- Never add a paper that has no evidence of existence.

## Step 2 — Extract

Create one row per paper. Fill every agreed column or use `—` when the source does not provide the
information. Do not turn a recap, count, or candidate list into the primary output.

### Default columns

| Column | Required content |
|---|---|
| Title & Authors | Title and concise author list; use `et al.` after six authors |
| Journal | Journal name |
| Year | Publication year |
| Purpose | Study purpose from the abstract or introduction |
| Method (Variables/Samples) | Design, variables, sample, instruments, and analysis |
| Key Findings | Main findings and reported values |
| Limitations | Limitations stated by the authors |
| Gaps | Gap addressed by the paper, unless another meaning is selected |
| Theory Used | Theory or conceptual framework and its role |
| Novelty/Contribution | Author-stated novelty or contribution |
| Future Studies | All stated future-work recommendations |
| DOI & Publisher | DOI and publisher with verification status |

### Provenance

Every factual sentence must end with a provenance marker:

```text
[AB]      Abstract or search metadata
[I-2]     Introduction, paragraph 2
[M-3]     Methods, paragraph 3
[R-1]     Results, paragraph 1
[D-2]     Discussion, paragraph 2
[L-1]     Limitations, paragraph 1
[C-1]     Conclusion, paragraph 1
[F-1]     Future Work, paragraph 1
```

Use `[AB]` for search-only evidence. Do not claim full-text methods, results, limitations, or
future work when only an abstract is available. Use `(summarized)` for explicit inference and
never use inference to manufacture missing facts.

## Step 3 — Build and export

1. Build `papers.json` as the master data source.
2. Render `literature_table.md` with one row per paper.
3. Add search metadata and the provenance legend above or below the table.
4. Run the export script only after validating JSON:

```bash
python3 scripts/export_formats.py papers.json \
  --formats csv,xlsx,bib,xml,ris \
  --out . \
  --prefix literature_table
```

If `openpyxl` is missing, install it with `python3 -m pip install openpyxl`, or provide CSV and
clearly report that XLSX was not generated.

## Step 4 — Validate

Load `protocols/output-guardrails.md`. For substantial output, also load
`protocols/evaluation.md` and `references/output-rubric.md`.

Before delivery, verify:

- every row has a source and correct metadata;
- every factual sentence has provenance;
- claims preserve source scope and modality;
- unavailable values use `—`;
- unresolved sources use `UNVERIFIED`;
- no papers, findings, numbers, citations, quotations, DOI values, or quartiles were invented;
- `papers.json`, Markdown, CSV/XLSX, BibTeX, XML, and RIS agree in count and bibliographic values;
- JSON and XML parse, RIS contains `TY` and `ER`, and BibTeX contains valid entries.

Report:

```text
papers_checked: N
metadata_mismatches: N
claims_without_provenance: N
unverified_sources: N
export_mismatches: N
flags: N
status: PASS | PASS_WITH_FLAGS | FAIL
```

Any fabricated source/content, unsupported finding, missing required provenance, or master/export
mismatch is a hard failure. `PASS_WITH_FLAGS` is allowed only for explicitly reported unresolved
source limitations.

## Handling missing or ambiguous information

- **Unclear scope, mode, columns, or filters**: Ask once before acquisition (Step 0). If the user asks to proceed with defaults, use 10–15 papers (Search), all eligible files (Folder), the 12 default columns, the last 5 years, English papers, and Markdown output.
- **Unavailable field in a paper**: Mark the cell with `—`. Never guess or infer missing sample sizes, methods, theories, limitations, or findings.
- **Abstract-only access (no full text)**: Extract only what is explicitly stated in the abstract/metadata and tag with `[AB]`. Mark full-text-only columns that are absent from the abstract as `—`.
- **Unresolved DOI or unverified bibliographic metadata**: Preserve the available source text and mark the status `UNVERIFIED — check manually`. Never fabricate a DOI, volume, issue, page range, or quartile.
- **Scanned or unreadable PDFs**: Report the unreadable file to the user and use `—` for unavailable fields rather than guessing from the title.

## Common mistakes to avoid

- **Replacing the table with a prose summary or candidate list**: The primary deliverable must always be a complete, one-row-per-paper synthesis table.
- **Inventing papers, DOIs, quartiles, or statistics**: Never hallucinate citations or repair missing metadata from memory.
- **Claiming full-text provenance from an abstract**: Never attach `[M-1]` or `[R-1]` markers when only the abstract (`[AB]`) was read.
- **Omitting provenance markers**: Every factual extraction sentence in the table must end with a provenance tag (`[AB]`, `[I-2]`, `[M-3]`, `[R-1]`, `[D-2]`, `[L-1]`, `[C-1]`, `[F-1]`).
- **Diverging export files**: Never edit Markdown, CSV, XLSX, BibTeX, XML, or RIS independently of `papers.json`; always generate exports from the validated `papers.json`.

## Non-negotiable rules

1. The primary output is a complete per-paper table.
2. Never invent papers, metadata, findings, methods, statistics, quotations, or recommendations.
3. Extract claims from the paper, not from the agent's opinion.
4. Preserve citations, provenance, scope, modality, terminology, numbers, and units.
5. Keep `papers.json` as the single source of truth.
6. Save artifacts in the user's working folder, not only in chat.
7. Include search date, sources, filters, and keyword combinations for reproducibility.
