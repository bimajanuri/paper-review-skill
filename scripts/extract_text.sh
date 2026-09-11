#!/usr/bin/env bash
#
# extract_text.sh — Extract text from PDF/TeX files in a folder for paper-review skill.
#
# Usage:
#   ./extract_text.sh <folder-or-file.pdf>
#
# Behavior:
#   - Recursively walks the given path.
#   - For every *.pdf it writes a sibling <name>.txt via pdftotext (poppler-utils).
#   - Logs progress to stderr; prints a summary at the end.
#
# Dependencies:
#   - pdftotext  (poppler-utils)  — install on macOS: `brew install poppler`
#
# Limits:
#   - Scanned/OCR-only PDFs may produce empty text. Report them so the agent can
#     fall back to metadata or ask the user about OCR.

set -u

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  echo "usage: $0 <folder-or-file.pdf>" >&2
  exit 1
fi

if ! command -v pdftotext >/dev/null 2>&1; then
  echo "ERROR: pdftotext not found. Install poppler-utils: 'brew install poppler' (macOS) or 'apt install poppler-utils' (Linux)." >&2
  exit 1
fi

index=0
empty=0
scanned=0

process_file() {
  local pdf="$1"
  local txt="${pdf%.pdf}.txt"

  if [ -f "$txt" ] && [ -s "$txt" ]; then
    echo "SKIP  (txt exists): $pdf" >&2
    return
  fi

  if pdftotext -layout "$pdf" "$txt" 2>/dev/null; then
    if [ -s "$txt" ]; then
      index=$((index + 1))
      echo "OK    ($(wc -l < "$txt") lines): $pdf" >&2
    else
      empty=$((empty + 1))
      rm -f "$txt"
      echo "EMPTY (likely scanned/OCR): $pdf" >&2
    fi
  else
    rm -f "$txt"
    echo "FAIL  : $pdf" >&2
  fi
}

if [ -d "$TARGET" ]; then
  while IFS= read -r -d '' f; do
    process_file "$f"
  done < <(find "$TARGET" -type f -iname '*.pdf' -print0)
elif [ -f "$TARGET" ]; then
  process_file "$TARGET"
else
  echo "ERROR: no such file or folder: $TARGET" >&2
  exit 1
fi

echo
echo "Summary: $index extracted | $empty empty/scanned+failed | target: $TARGET"
if [ "$empty" -gt 0 ]; then
  echo "Hint: $empty PDF(s) produced no text — likely scans. Consider OCR or metadata fallback."
fi