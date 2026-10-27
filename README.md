# Paper Review Skill

Paper Review helps AI agents turn a set of academic papers into a clear, traceable literature
matrix. It can search online sources, read a local collection of PDF or LaTeX files, or combine
both. The workflow keeps `papers.json` as the master dataset and can produce Markdown, CSV, XLSX,
BibTeX, EndNote XML, and RIS outputs from the same records.

## Features

- Search, Folder, and Hybrid input modes, with deduplication by DOI or normalized title.
- Twelve default extraction columns, plus any custom columns the user needs.
- Source markers such as `[AB]`, `[M-2]`, and `[R-1]` so each factual extraction can be traced back
  to the paper.
- OpenAlex, Semantic Scholar, arXiv, Crossref, DOI, publisher, and web-source workflows.
- Scopus quartile tagging and multi-round search, including backward/forward snowballing.
- PDF extraction through `scripts/extract_text.sh` and direct LaTeX reading.
- Anti-fabrication rules using `—`, `(summarized)`, and `UNVERIFIED` status markers.
- Output guardrails for metadata, provenance, claim scope, and export consistency.
- Evaluation rubric with hard-failure precedence and `PASS`, `PASS_WITH_FLAGS`, or `FAIL` status.

## Workflow

```text
STEP 0: CLARIFY   → input mode, topic, target count, columns, filters, language, export format
STEP 1: ACQUIRE   → collect, deduplicate, and verify papers
STEP 2: EXTRACT   → read abstracts/full text and populate every agreed field
STEP 3: BUILD     → create papers.json, render Markdown, and export requested formats
STEP 4: VALIDATE  → run guardrails, evaluation, DOI checks, and quality gates
```

The main deliverable is always a complete, one-row-per-paper table. Candidate lists and aggregate
statistics are useful supporting material, but they never replace the table.

## Compatibility and prerequisites

Paper Review follows the folder-based Agent Skills convention. The host must be able to discover a
directory containing `SKILL.md` and read its `references/`, `protocols/`, `templates/`, and
`scripts/` files. No API key, database, background service, or operating-system-specific runtime
is required. Install the complete directory so every referenced module remains available.

| Host | Project path | Global path | Activation and verification |
|---|---|---|---|
| Claude Code | `.claude/skills/paper-review/` | `~/.claude/skills/paper-review/` | Request a literature matrix; use `/skills` if available |
| OpenCode | `.opencode/skills/paper-review/` or `.agents/skills/paper-review/` | `~/.config/opencode/skills/paper-review/` | Enable the `skill` tool and request `paper-review` |
| Gemini CLI | `.gemini/skills/paper-review/` or `.agents/skills/paper-review/` | `~/.gemini/skills/paper-review/` | Run `/skills`, then request a paper review |
| GitHub Copilot CLI | `.github/skills/paper-review/` or `.agents/skills/paper-review/` | `~/.copilot/skills/paper-review/` | Run `/skills reload`, then `/skills info paper-review` |
| Antigravity | `.agents/skills/paper-review/` | `~/.gemini/config/skills/paper-review/` | Start a matching literature-review task |
| Gemini Apps (Web, Mac, Mobile) | `gemini.google.com` → **Customize** → **Skills** → **Create** → **Upload** | Product-managed (Personal Google Account 18+, Keep Activity on) | Upload folder or `.zip` with `SKILL.md` in root; invoke via `/` or `@` or automatic matching |
| ChatGPT Skills | Upload the complete directory or ZIP via Skills UI | Product-managed | Import it where Skills are enabled and invoke via `/` or natural language |
| Codex, Cursor, Windsurf, other compatible hosts | Host-specific path or `.agents/skills/paper-review/` | Host-specific | Reload skills and verify discovery |

ChatGPT Skills availability and upload permissions depend on the account, workspace, and product
surface. If a host does not support folder-based Skills, use its documented import or project-file
mechanism and provide `SKILL.md` together with every referenced module.

### Optional prerequisites

- **Poppler** (`pdftotext`) for PDF extraction: `brew install poppler` on macOS.
- **Python 3** for the export script.
- **openpyxl** for XLSX output: `python3 -m pip install openpyxl`.
- **Web access** for live metadata, DOI, publisher, and quartile verification.
- **Zotero, EndNote, or Mendeley** for importing generated bibliography files.

## Installation

Use the repository directory as the source path in the commands below.

### Claude Code

```bash
mkdir -p ~/.agents/skills ~/.claude/skills
ln -s /path/to/paper-review ~/.agents/skills/paper-review
ln -s ~/.agents/skills/paper-review ~/.claude/skills/paper-review
# Or copy directly:
cp -R /path/to/paper-review ~/.claude/skills/paper-review
```

### OpenCode

```bash
mkdir -p ~/.config/opencode/skills
cp -R /path/to/paper-review ~/.config/opencode/skills/paper-review
```

### Gemini CLI

```bash
mkdir -p ~/.gemini/skills
cp -R /path/to/paper-review ~/.gemini/skills/paper-review
# In Gemini CLI:
/skills
```

### GitHub Copilot CLI

```bash
mkdir -p ~/.copilot/skills
cp -R /path/to/paper-review ~/.copilot/skills/paper-review
# In Copilot CLI:
/skills reload
/skills info paper-review
```

### Antigravity

```bash
mkdir -p ~/.gemini/config/skills
cp -R /path/to/paper-review ~/.gemini/config/skills/paper-review
```

### Gemini Apps (Web, Mac, and Mobile) — Upload ZIP Method

Gemini Apps (`gemini.google.com`, the Gemini Mac app, and the mobile app) support installing custom skills by uploading a folder or `.zip` archive (requires a personal Google Account 18+ with **Keep Activity** turned on).

Per Google's upload requirements ([Create & manage skills for Gemini Apps](https://support.google.com/gemini/answer/17094296)):
- `SKILL.md` must be located in the **root (main) folder** of the uploaded folder or `.zip` archive.
- The skill `name` inside `SKILL.md` must be lowercase with hyphens (`paper-review`).
- All files in the package (`.md`, `.py`, `.sh`, `.json`) are supported plain-text formats and must total under 100 MB.
- Exclude hidden binary/OS metadata files (such as `.DS_Store`, `.git/`, `.pyc`, or `__MACOSX`) so the upload validation does not fail.

**Step 1: Create a clean `.zip` archive (with `SKILL.md` at the root)**

```bash
cd /path/to/paper-review
zip -r -X paper-review-gemini.zip \
  SKILL.md protocols references templates scripts tests \
  -x "*.DS_Store" -x "__MACOSX/*" -x "*.git*" -x "*.pyc"
```

*(Alternatively, you can upload the `paper-review` folder directly as long as it contains no hidden `.DS_Store` or `.git` files.)*

**Step 2: Upload to Gemini Web (`gemini.google.com`)**

1. Go to [gemini.google.com](https://gemini.google.com) (or open the Gemini app on Mac).
2. On the left sidebar, click **Customize** (if you don't see it, first click **More**) → **Skills**.
3. At the top of the Skills page, click **Create** → **Upload**.
4. Select `paper-review-gemini.zip` (or the `paper-review/` folder) and click **Open**.
5. Review the imported skill details and click **Create** at the top.
6. **Usage**: In any chat or task thread, type `/` (or `@`) and select `paper-review`, or describe your literature review request in natural language — Gemini automatically applies activated skills when relevant.

### ChatGPT Skills — Upload ZIP Method

ChatGPT Skills can be installed by uploading a `.zip` package on accounts and workspaces with the Skills feature enabled (or attached directly in chat sessions if the Skills UI is unavailable).

**Step 1: Create a clean `.zip` package**

You can package either the root files (`paper-review-gemini.zip` above) or the complete `paper-review/` directory without hidden OS/Git files:

```bash
zip -r -X paper-review.zip paper-review \
  -x "*/.git/*" -x "*/.DS_Store" -x "__MACOSX/*" -x "*.pyc"
```

**Step 2: Upload to ChatGPT**

1. In ChatGPT, open **Skills** from the sidebar or profile menu.
2. Click **Create** → **Upload from your computer**, and select `paper-review.zip`.
3. Enable the skill for your conversation or workspace.
4. **Usage**: Invoke the skill with `/` or natural-language prompts such as:

```text
Use the paper-review skill in Search mode. Review 15 papers on [topic] from the last five years,
preserve provenance markers for every factual sentence, verify DOI metadata, and build the synthesis table.
```

If the Skills UI is not available on your plan, upload/attach the `.zip` archive (or the relevant Markdown files) directly in the chat message composer and instruct ChatGPT to read and follow `SKILL.md`.

> **Note:** ChatGPT may scan an uploaded skill and mark it as **Needs Review** or **Blocked**. This is a workspace/product safety check rather than an issue with the Agent Skills format; review workspace permissions before retrying.

### Other compatible hosts

Copy the complete directory into the host's documented skills folder, reload the host, and verify
that `paper-review` is discoverable. Copying only `SKILL.md` is insufficient for full extraction
and export behavior.

## Usage

The skill activates automatically when a request clearly asks for a literature matrix, paper-review
table, paper synthesis, PDF/LaTeX extraction, or bibliography export. Use natural language, or name
`paper-review` explicitly when you want to make the workflow unambiguous. If the request leaves the
mode, scope, columns, filters, or export formats open, the skill clarifies those choices first.

### Search mode

```text
Use paper-review in Search mode. Review 15 papers on [topic] from the last five years.
Lock the columns and filters first. Preserve provenance for every factual sentence,
verify DOI metadata, build `papers.json`, run the output guardrails, and report
`PASS`, `PASS_WITH_FLAGS`, or `FAIL` before exporting CSV, XLSX, BibTeX, XML, or RIS.
```

### Folder mode

```text
Use paper-review in Folder mode. Review every PDF and LaTeX paper in [folder].
Extract the agreed fields with provenance markers. Use `—` when information is unavailable,
verify metadata where possible, build the complete per-paper table, and report the final
guardrail status.
```

### Hybrid mode

```text
Use paper-review in Hybrid mode. Combine verified search results about [topic] with
the papers in [folder]. Deduplicate by DOI, then normalized title; prefer local full text;
build `papers.json` and `literature_table.md`; export the requested formats only after validation.
```

### Targeted requests

```text
Create a literature matrix with these additional columns: [columns].
```

```text
Export the validated papers.json to CSV, XLSX, BibTeX, EndNote XML, and RIS.
```

```text
Review this matrix for missing provenance, fabricated metadata, DOI mismatches,
unsupported findings, and inconsistencies across export formats.
```

## Default matrix columns

1. Title & Authors
2. Journal
3. Year
4. Purpose
5. Method (Variables/Samples)
6. Key Findings
7. Limitations
8. Gaps
9. Theory Used
10. Novelty/Contribution
11. Future Studies
12. DOI & Publisher

Use `—` for every unavailable extraction value. Search-only records must not claim full-text
methods or findings that are absent from the available abstract or metadata.

## Repository structure

```text
paper-review/
├── SKILL.md
├── protocols/
│   ├── output-guardrails.md
│   └── evaluation.md
├── references/
│   ├── search-sources.md
│   ├── extracting-papers.md
│   ├── table-builder.md
│   └── output-rubric.md
├── templates/paper_review_table_template.md
├── scripts/extract_text.sh
├── scripts/export_formats.py
└── tests/sample_papers.json
```

## Rules

1. The primary output is a complete per-paper table, not a candidate list or recap.
2. Never invent papers, DOI metadata, findings, methods, numbers, quotations, or recommendations.
3. Every factual extraction sentence must have a provenance marker.
4. Use `UNVERIFIED` for unresolved sources and `—` for unavailable data.
5. Keep `papers.json` as the single source of truth for every export.
6. Include the search date, sources, filters, and keyword combinations for reproducibility.
7. Run output guardrails before delivery and report the final status.

## License

Released under the [MIT License](LICENSE).
