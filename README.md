# Paper Review Skill

**Paper review and literature synthesis for AI agents.** This skill creates a structured
literature-review matrix from online searches, local PDF/LaTeX files, or both. It produces a
master `papers.json`, a Markdown table, and optional CSV, XLSX, BibTeX, EndNote XML, and RIS
exports.

## Features

- Search, Folder, and Hybrid input modes with DOI/title deduplication.
- Twelve default extraction columns plus user-defined custom columns.
- Source provenance markers such as `[AB]`, `[M-2]`, and `[R-1]` for every factual extraction.
- OpenAlex, Semantic Scholar, arXiv, Crossref, DOI, publisher, and web-source workflows.
- Scopus quartile tagging and multi-round search, including backward/forward snowballing.
- PDF extraction through `scripts/extract_text.sh` and direct LaTeX reading.
- Anti-fabrication rules with `—`, `(summarized)`, and `UNVERIFIED` status markers.
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

The complete output is always a per-paper table. Candidate lists and aggregate statistics are
supplementary and must not replace the table.

## Compatibility and prerequisites

This skill follows the folder-based Agent Skills convention. The host must discover a directory
containing `SKILL.md` and allow access to its `references/`, `protocols/`, `templates/`, and
`scripts/` files. There is no mandatory API key, database, runtime service, or OS-specific
dependency. Always install the complete directory.

| Host | Project path | Global path | Activation and verification |
|---|---|---|---|
| Claude Code | `.claude/skills/paper-review/` | `~/.claude/skills/paper-review/` | Request a literature matrix; use `/skills` if available |
| OpenCode | `.opencode/skills/paper-review/` or `.agents/skills/paper-review/` | `~/.config/opencode/skills/paper-review/` | Enable the `skill` tool and request `paper-review` |
| Gemini CLI | `.gemini/skills/paper-review/` or `.agents/skills/paper-review/` | `~/.gemini/skills/paper-review/` | Run `/skills`, then request a paper review |
| GitHub Copilot CLI | `.github/skills/paper-review/` or `.agents/skills/paper-review/` | `~/.copilot/skills/paper-review/` | Run `/skills reload`, then `/skills info paper-review` |
| Antigravity | `.agents/skills/paper-review/` | `~/.gemini/config/skills/paper-review/` | Start a matching literature-review task |
| ChatGPT Skills | Upload the complete directory or ZIP | Product-managed | Import it where Skills are enabled and invoke it |
| Codex, Cursor, Windsurf, other compatible hosts | Host-specific path or `.agents/skills/paper-review/` | Host-specific | Reload skills and verify discovery |

ChatGPT Skills availability and upload permissions depend on the account, workspace, and product
surface. If a host does not support folder-based Skills, use its documented import/project-files
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

### ChatGPT Skills

When Skills are enabled, upload `paper-review/` as a directory or ZIP. Preserve `SKILL.md`,
`protocols/`, `references/`, `templates/`, `scripts/`, and `tests/`. If Skills are unavailable,
use the platform's custom-instructions or project-files mechanism with the complete directory.

### Other compatible hosts

Copy the complete directory into the host's documented skills folder, reload the host, and verify
that `paper-review` is discoverable. Copying only `SKILL.md` is insufficient for full extraction
and export behavior.

## Activation example

```text
Use the paper-review skill. Review 15 papers on [topic] using Search mode.
Lock the columns and filters first, preserve provenance for every factual sentence,
verify DOI metadata, build papers.json, run output guardrails, and report
PASS, PASS_WITH_FLAGS, or FAIL before exporting CSV, XLSX, BibTeX, XML, or RIS.
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

Every unavailable extraction value must be `—`. Search-only records must not claim full-text
methods or findings that are not present in the available abstract or metadata.

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
