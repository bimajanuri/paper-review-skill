# Table Builder — Render & Export Tabel Review

Panduan merakit output tabel (Markdown) **dan export 5 format** (CSV / XLSX / BIB / XML / RIS) dari
hasil ekstraksi — **Literature Review / Data Extraction** (synthesis matrix) ala reference-manager AI.

## 1. Konsep: Satu Data → Banyak Format

Seluruh format diturunkan dari **satu file master** `papers.json`. Agent membangun JSON ini di
Step 2/3, lalu `scripts/export_formats.py` menurunkan semua format dari sana.

```text
papers.json ──► literature_table.md   (tabel markdown)
            ──► literature_table.csv  (Excel/Google Sheets)
            ──► literature_table.xlsx (Excel terformat: sheet Papers + Metadata)
            ──► literature_table.bib  (BibTeX, import ke Zotero/JabRef/Overleaf)
            ──► literature_table.xml  (EndNote XML, import ke EndNote/Zotero)
            ──► literature_table.ris  (RIS JOUR, import ke Zotero/Mendeley/EndNote)
```

## 2. Skema `papers.json`

```json
{
  "meta": {
    "mode": "Search", "topic": "...", "query": "...", "date": "2026-09-11",
    "target": 15, "sources": "OpenAlex", "note": "..."
  },
  "papers": [
    {
      "title": "...",
      "authors": ["Surname, Given", "Surname2, Given2"],
      "year": "2026",
      "journal": "...", "volume": "", "issue": "", "pages": "",
      "doi": "10.xxxx/...", "publisher": "...", "url": "",
      "abstract": "...", "keywords": ["k1", "k2"],
      "purpose": "...", "method": "...", "key_findings": "...",
      "limitations": "...", "gaps": "...", "theory": "...",
      "novelty": "...", "future_work": "...",
      "custom": { "<Label Kolom Custom>": "..." }
    }
  ]
}
```

Aturan:
- Field **biblio** (title/authors/year/journal/volume/issue/pages/doi/publisher/url/abstract/keywords)
  diisi dari metadata API/file. Tidak tersedia → **string kosong** (agar tidak ikut export sitasi).
- Field **ekstraksi** (purpose/method/key_findings/limitations/gaps/theory/novelty/future_work + custom)
  tidak tersedia → `—` di tabel, tidak mengarang.
- `authors` berupa **list** `["Surname, Given", ...]` — wajib untuk BibTeX/RIS/XML yang benar.

## 3. Kolom Default (Synthesis Matrix)

Urutan kolom yang dirender ke tabel/CSV/XLSX (label → key):

| Label di tabel | Key di JSON |
|----------------|-------------|
| No | (indeks baris) |
| Title & Authors | `authors_title` (komposisi: penulis — "judul") |
| Journal | `journal` |
| Year | `year` |
| Purpose | `purpose` |
| Method (Variables/Samples) | `method` |
| Key Findings | `key_findings` |
| Limitations | `limitations` |
| Gaps (yang di-address) | `gaps` |
| Theory Used | `theory` |
| Novelty/Contribution | `novelty` |
| Future Studies | `future_work` |
| DOI & Publisher | `source` (komposisi: DOI: ... \| Penerbit) |

Kolom custom ditambahkan dari object `custom` tiap paper; urutannya mengikuti urutan pertama muncul.
Agent dapat menambah kolom (mis. `Citations`, `Sampling Method`) dengan memasukkan label sama di semua
paper. `DEFAULT_COLS` di `export_formats.py` dapat dioverride — cukup tambahkan array `columns` di JSON
(jika dipakai, tiap elemen `{"label":"...","key":"key_di_paper"}` atau string = label dengan key sama).

## 4. Render Markdown

```markdown
| No | Title & Authors | Journal | Year | Purpose | ... |
|----|-----------------|---------|-------|---------|-----|
| 1  | Smith, John et al. — "..." | Jurnal | 2026 | Penelitian bertujuan ... [I-1] | ... |
```

- Sel berisi **2–5 kalimat lengkap** (komprehensif, ala data extraction reference-manager AI), bukan frasa pendek —
  lihat `references/extracting-papers.md` §3a. Setiap kalimat/klaim diakhiri **penanda sumber**
  `[KODE-n]` (bagian + nomor paragraf), mis. `[M-2]`, `[R-1][R-3]`.
- Jangan pakai baris baru dalam sel markdown — kalimat-kalimat digabung dalam satu baris sel.
- Di atas tabel: **Metadata Pencarian** (mode, topik, query, jumlah target/jumlah baris, tanggal, sumber).
- Di bawah tabel: **Legenda Penanda Sumber**:

  ```markdown
  **Legenda — kode bagian paper:** AB=Abstract · I=Introduction · M=Method · R=Results ·
  D=Discussion · L=Limitations · C=Conclusion · F=Future Work
  (penanda `[M-2]` = klaim dari bagian Method, paragraf 2)
  ```

  Serta legenda lain: `—` (data tak tersedia), `(diringkas)` (inferensi), `[±n]` (perkiraan paragraf),
  `UNVERIFIED` (DOI belum diverifikasi).

## 5. Export 5 Format

```bash
python3 scripts/export_formats.py papers.json \
    --formats csv,xlsx,bib,xml,ris \
    --out . \
    --prefix literature_table
```

| opsi | default | keterangan |
|------|---------|------------|
| `--formats` | `csv,xlsx,bib,xml,ris` | subset format yang diinginkan, pisahkan koma |
| `--out` | `.` | folder output |
| `--prefix` | `literature_table` | nama dasar file output |

Detail tiap format:
- **`.csv`** — header = kolom tabel; UTF-8 dengan BOM (agar karakter non-ASCII terbaca benar di Excel).
- **`.xlsx`** — butuh `openpyxl` (`pip3 install openpyxl` bila belum ada). Sheet `Papers`: header
  terformat (bold + fill biru), wrap text, freeze top row, autofilter, lebar kolom otomatis.
  Sheet `Metadata`: isi `meta`.
- **`.bib`** — `@article{key, ...}` dengan `author` joined ` and `, `doi`, `journal`, `year`,
  `volume/number/pages`, `publisher`, `abstract`, `keywords`; kolom ekstraksi digabung ke field `note`.
- **`.xml`** — **EndNote XML**: `<xml><records><record>` dengan `<ref-type name="Journal Article">17</ref-type>`,
  contributors/authors, titles/title, periodicals/full-title, dates/year, volume/number/pages,
  publisher, abstract, keywords, `<electronic-resource-num>` untuk DOI, `<url>`, `<notes>`.
- **`.ris`** — `TY  - JOUR`, `AU` per penulis, `TI`, `JO/JF`, `PY`, `VL`, `IS`, `SP/EP`, `DO`, `PB`,
  `AB`, `KW`, `UR`, `N1` (notes kolom ekstraksi), diakhiri `ER  - `.

## 6. Validasi Sebelum Menyerahkan

1. `papers.json` ter-parse (`python3 -c "import json;json.load(open('papers.json'))"`).
2. Jumlah baris tabel == jumlah paper lolos (sesuai triase Step 4).
3. Tidak ada sel kosong misterius — selalu `—` saat data tidak tersedia.
4. DOI konsisten (`DOI: 10.xxxx/...`).
5. Spot-check file export: .bib terbaca, .ris punya `TY`/`ER`, .xml valid XML, .xlsx terbuka
   (verifikasi cepat dengan openpyxl/parser bila tersedia).
6. Jika akan diimpor ke reference manager, sarankan user menguji satu file (Zotero/Mendeley).

## 7. Output

```
papers.json           — master data (wajib disimpan)
literature_table.md   — tabel final markdown
literature_table.csv / .xlsx / .bib / .xml / .ris — export sesuai permintaan
```