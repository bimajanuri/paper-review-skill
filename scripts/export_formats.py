#!/usr/bin/env python3
"""
export_formats.py — Export paper-review table to multiple formats.

Reads a papers.json file produced by the paper-review skill and writes:
  CSV, XLSX (Excel), BIB (BibTeX), XML (EndNote XML), RIS

One-command export: `python3 export_formats.py papers.json`

Usage:
  python3 export_formats.py papers.json \
      [--formats csv,xlsx,bib,xml,ris] \
      [--out DIR] \
      [--prefix literature_table]

Input JSON schema:
{
  "meta": { "mode": "...", "topic": "...", "query": "...", "date": "...",
            "target": N, "sources": "...", "note": "..." },
  "papers": [
    {
      "title": "...", "authors": ["Surname, Given", ...],
      "year": "2026", "journal": "...", "volume": "", "issue": "", "pages": "",
      "doi": "10.xxxx/...", "publisher": "...", "url": "", "abstract": "",
      "keywords": ["a", "b"],
      "purpose": "...", "method": "...", "key_findings": "...",
      "limitations": "...", "gaps": "...", "theory": "...",
      "novelty": "...", "future_work": "...",
      "custom": { "<Custom Column>": "..." }
    }, ...
  ]
}

BibTeX/RIS/XML use the bibliographic fields (title, authors, year, journal,
volume, issue, pages, doi, publisher, url, abstract, keywords). The extraction
columns (purpose, method, key_findings, limitations, gaps, theory, novelty,
future_work, custom) are carried as abstract/notes where the format allows.
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata

EM_DASH = "\u2014"

# Default column order (label -> field key).
# "authors_title", "source" are composed; "no" is the row index.
DEFAULT_COLS = [
    ("No", "no"),
    ("Title & Authors", "authors_title"),
    ("Journal", "journal"),
    ("Year", "year"),
    ("Purpose", "purpose"),
    ("Method (Variables/Samples)", "method"),
    ("Key Findings", "key_findings"),
    ("Limitations", "limitations"),
    ("Gaps (yang di-address)", "gaps"),
    ("Theory Used", "theory"),
    ("Novelty/Contribution", "novelty"),
    ("Future Studies", "future_work"),
    ("DOI & Publisher", "source"),
]

GOOD_FILE = re.compile(r"[^A-Za-z0-9._-]")


def t(obj, key, default="\u2014"):
    v = obj.get(key)
    if v is None:
        return default
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    v = str(v).strip()
    return v if v else default


def authors_str(p):
    authors = p.get("authors") or []
    if not authors:
        return "\u2014"
    if len(authors) > 6:
        return f"{authors[0]} et al."
    return ", ".join(authors)


def compose_value(p, key, idx):
    if key == "no":
        return str(idx + 1)
    if key == "authors_title":
        return f'{authors_str(p)} — "{t(p, "title")}"'
    if key == "source":
        doi = t(p, "doi")
        pub = t(p, "publisher")
        journal = t(p, "journal")
        parts = []
        if doi != "\u2014":
            parts.append(f"DOI: {doi}")
        if pub != "\u2014":
            parts.append(pub)
        elif journal != "\u2014":
            parts.append(journal)
        return " | ".join(parts)
    if key in p:
        return t(p, key)
    return "\u2014"


def build_rows(papers, cols):
    rows = []
    for idx, p in enumerate(papers):
        row = {}
        for label, key in cols:
            if key == "custom":
                continue
            row[label] = compose_value(p, key, idx)
        for ckey, cval in (p.get("custom") or {}).items():
            row[ckey] = str(cval) if cval else "\u2014"
        rows.append(row)
    return rows


def header_row(cols, custom_keys):
    return [label for label, _ in cols] + list(custom_keys)


def paper_custom_keys(papers):
    keys = []
    for p in papers:
        for k in (p.get("custom") or {}):
            if k not in keys:
                keys.append(k)
    return keys


def bibtex_key(p):
    year = t(p, "year", "")
    authors = p.get("authors") or []
    base = ""
    if authors:
        base = re.split(r"[\s,]+", authors[0].strip())[0].lower()
    title_start = ""
    title = t(p, "title", "")
    if title != "\u2014":
        title_start = re.split(r"\W+", title.lower())[0]
    stem = "".join(filter(str.isalnum, base + year + title_start)) or "paper"
    return stem


def export_bibtex(papers, path):
    lines = []
    for p in papers:
        authors = p.get("authors") or []
        author_bib = " and ".join(authors) or "\u2014"
        fields = [
            ("author", author_bib),
            ("title", t(p, "title").strip('"')),
            ("journal", t(p, "journal")),
            ("year", t(p, "year", "")),
        ]
        for k in ("volume", "number", "pages"):
            v = t(p, k, "")
            if v:
                fields.append((k, v))
        for k in ("doi", "publisher", "url"):
            v = t(p, k, "")
            if v and v != "\u2014":
                fields.append((k, v))
        abstract = t(p, "abstract", "")
        if abstract != "\u2014":
            fields.append(("abstract", abstract))
        kws = p.get("keywords") or []
        if kws:
            fields.append(("keywords", ", ".join(kws)))
        notes = extraction_notes(p)
        if notes:
            fields.append(("note", notes))
        lines.append(f"@article{{{bibtex_key(p)},")
        for k, v in fields:
            v = v.replace("\x00", "")
            lines.append(f"  {k:<10} = {{{v}}},")
        lines.append("}")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def extraction_notes(p):
    parts = []
    for label, key in [
        ("Purpose", "purpose"),
        ("Method", "method"),
        ("Key Findings", "key_findings"),
        ("Limitations", "limitations"),
        ("Gaps", "gaps"),
        ("Theory", "theory"),
        ("Novelty", "novelty"),
        ("Future Work", "future_work"),
    ]:
        v = t(p, key, "")
        if v and v != "\u2014":
            parts.append(f"{label}: {v}")
    return " | ".join(parts)


def ris_wrap(f, tag, value):
    if value is None or value == "\u2014":
        return
    value = str(value)
    first = True
    while value:
        chunk = value[:250]
        value = value[250:]
        prefix = f"{tag}  - " if first else "     "
        f.write(f"{prefix}{chunk}\n")
        first = False


def export_ris(papers, path):
    with open(path, "w", encoding="utf-8") as f:
        for p in papers:
            f.write("TY  - JOUR\n")
            for a in p.get("authors") or []:
                ris_wrap(f, "AU", a)
            ris_wrap(f, "TI", t(p, "title"))
            ris_wrap(f, "JO", t(p, "journal"))
            ris_wrap(f, "JF", t(p, "journal"))
            ris_wrap(f, "PY", t(p, "year", ""))
            ris_wrap(f, "VL", t(p, "volume", ""))
            ris_wrap(f, "IS", t(p, "number", ""))
            pages = t(p, "pages", "")
            if pages:
                pages = pages.replace("-", "\u2013")
                if "\u2013" in pages:
                    sp, _, ep = pages.partition("\u2013")
                    ris_wrap(f, "SP", sp)
                    ris_wrap(f, "EP", ep)
                else:
                    ris_wrap(f, "SP", pages)
            ris_wrap(f, "DO", t(p, "doi", ""))
            ris_wrap(f, "PB", t(p, "publisher", ""))
            ris_wrap(f, "AB", t(p, "abstract", ""))
            for kw in p.get("keywords") or []:
                ris_wrap(f, "KW", kw)
            ris_wrap(f, "UR", t(p, "url", ""))
            notes = extraction_notes(p)
            ris_wrap(f, "N1", notes)
            f.write("ER  - \n\n")


def xml_escape(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def export_xml(papers, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<xml>\n  <records>\n")
        for p in papers:
            f.write("    <record>\n")
            f.write('      <ref-type name="Journal Article">17</ref-type>\n')
            f.write("      <contributors><authors>\n")
            for a in p.get("authors") or []:
                f.write(f"        <author>{xml_escape(a)}</author>\n")
            f.write("      </authors></contributors>\n")
            f.write(f"      <titles><title>{xml_escape(t(p, 'title'))}</title></titles>\n")
            f.write(
                f"      <periodicals><full-title>{xml_escape(t(p, 'journal'))}</full-title></periodicals>\n"
            )
            f.write(f"      <dates><year>{xml_escape(t(p, 'year', ''))}</year></dates>\n")
            for tag, key in (("volume", "volume"), ("number", "number"), ("pages", "pages")):
                v = t(p, key, "")
                if v:
                    f.write(f"      <{tag}>{xml_escape(v)}</{tag}>\n")
            f.write(f"      <publisher>{xml_escape(t(p, 'publisher', ''))}</publisher>\n")
            abstract = t(p, "abstract", "")
            if abstract != "\u2014":
                f.write(f"      <abstract>{xml_escape(abstract)}</abstract>\n")
            kws = p.get("keywords") or []
            if kws:
                f.write(f"      <keywords>{xml_escape(', '.join(kws))}</keywords>\n")
            doi = t(p, "doi", "")
            if doi and doi != "\u2014":
                f.write(f"      <electronic-resource-num>{xml_escape(doi)}</electronic-resource-num>\n")
            url = t(p, "url", "")
            if url and url != "\u2014":
                f.write(f"      <url><related-urls><url>{xml_escape(url)}</url></related-urls></url>\n")
            notes = extraction_notes(p)
            if notes:
                f.write(f"      <notes>{xml_escape(notes)}</notes>\n")
            f.write("    </record>\n")
        f.write("  </records>\n</xml>\n")


def export_csv(rows, cols, custom_keys, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header_row(cols, custom_keys))
        w.writeheader()
        for row in rows:
            w.writerow(row)


def export_xlsx(papers, rows, cols, custom_keys, meta, path):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
    except ImportError:
        print(
            "WARN: openpyxl not installed — skipping xlsx. "
            "Install with: pip3 install openpyxl",
            file=sys.stderr,
        )
        return False

    headers = header_row(cols, custom_keys)
    wb = Workbook()
    ws = wb.active
    ws.title = "Papers"

    fill = PatternFill("solid", fgColor="1F4E78")
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)

    for row in rows:
        ws.append([row.get(h, "\u2014") for h in headers])

    widths = {}
    for h in headers:
        widths[h] = min(max(len(str(h)), 12), 40)
    for row in rows:
        for h in headers:
            v = str(row.get(h, ""))
            widths[h] = max(widths[h], min(len(v), 60))
    for i, h in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = widths[h] + 2
    for r in range(2, ws.max_row + 1):
        for cell in ws[r]:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"

    if meta:
        wsm = wb.create_sheet("Metadata")
        for k, v in meta.items():
            wsm.append([str(k), str(v)])
        wsm.column_dimensions["A"].width = 16
        wsm.column_dimensions["B"].width = 60

    wb.save(path)
    return True


def main():
    ap = argparse.ArgumentParser(description="Export paper-review data to CSV/XLSX/BIB/XML/RIS")
    ap.add_argument("data", help="papers.json from the paper-review skill")
    ap.add_argument(
        "--formats",
        default="csv,xlsx,bib,xml,ris",
        help="comma-separated formats (default: all five)",
    )
    ap.add_argument("--out", default=".", help="output directory")
    ap.add_argument("--prefix", default="literature_table", help="output basename")
    args = ap.parse_args()

    with open(args.data, encoding="utf-8") as f:
        data = json.load(f)

    papers = data.get("papers", [])
    meta = data.get("meta", {})
    cols = DEFAULT_COLS
    if "columns" in data:
        cols = []
        for c in data["columns"]:
            if isinstance(c, str):
                cols.append((c, c))
            else:
                cols.append((c.get("label"), c.get("key", c.get("label"))))

    custom_keys = paper_custom_keys(papers)
    rows = build_rows(papers, cols)
    os.makedirs(args.out, exist_ok=True)

    requested = [x.strip().lower() for x in args.formats.split(",") if x.strip()]
    done = []

    if "csv" in requested:
        p = os.path.join(args.out, args.prefix + ".csv")
        export_csv(rows, cols, custom_keys, p)
        done.append(p)
    if "xlsx" in requested:
        p = os.path.join(args.out, args.prefix + ".xlsx")
        if export_xlsx(papers, rows, cols, custom_keys, meta, p):
            done.append(p)
    if "bib" in requested:
        p = os.path.join(args.out, args.prefix + ".bib")
        export_bibtex(papers, p)
        done.append(p)
    if "xml" in requested:
        p = os.path.join(args.out, args.prefix + ".xml")
        export_xml(papers, p)
        done.append(p)
    if "ris" in requested:
        p = os.path.join(args.out, args.prefix + ".ris")
        export_ris(papers, p)
        done.append(p)

    print(f"Exported {len(done)} file(s) for {len(papers)} paper(s):")
    for p in done:
        print("  " + p)


if __name__ == "__main__":
    main()