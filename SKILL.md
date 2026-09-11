---
name: paper-review
description: |
  Menghasilkan tabel review literatur akademik (synthesis matrix / literature review matrix) dari (a) pencarian online berdasarkan topik + kata kunci + jumlah target, atau (b) folder lokal berisi paper berformat PDF/LaTeX, atau (c) kombinasi keduanya. Output: tabel markdown + export CSV, Excel (XLSX), BibTeX (BIB), XML (EndNote), dan RIS. Kolom default: Title & Authors, Journal, Year, Purpose, Method (Variables/Samples), Key Findings, Limitations, Gaps, Theory Used, Novelty/Contribution, Future Studies, DOI & Publisher — plus kolom custom apa pun. Generates a structured literature review synthesis matrix from online search or a local PDF/LaTeX folder, exportable to CSV/XLSX/BIB/XML/RIS. Trigger: "literature review", "tabel review paper", "tabel literatur", "review paper di folder ini", "cari paper tentang X sebanyak N", "literature matrix", "synthesize papers", "review jurnal", "export ris", "bibtex", "subset of academic-writing-skill".
---

# Paper Review — Review & Sintesis Literatur

Skill ini membuat **tabel review** terstruktur dari paper akademik — format **Literature Review /
Data Extraction** (synthesis matrix): tabel silang dengan blok sitasi + blok ekstraksi,
dan **ekspor 5 format** (CSV, Excel XLSX, BibTeX, XML, RIS). Merupakan subset terfokus dari
[bimajanuri/academic-writing-skill](https://github.com/bimajanuri/academic-writing-skill): hanya bagian
pengumpulan literatur + ekstraksi metadata + penyusunan tabel (setara Tahap 1 "Explorasi"), tanpa
pipeline penulisan/sitasi/revisi.

Bahasa: konten skill **bilingual** (Indonesia utama, English ringkas). Output mengikuti preferensi user per sesi.

## Input Modes

| Mode | Kapan dipakai | Sumber paper |
|------|--------------|--------------|
| **A. Search** | User memberi topik + kata kunci (+ jumlah target) | Pencarian online (OpenAlex / Semantic Scholar / arXiv / web tools) |
| **B. Folder** | User punya folder berisi paper `.pdf` / `.tex` | Baca file langsung dari folder |
| **C. Hybrid** | User minta gabungan keduanya | Hasil search + file folder dicampur, duplikat dihapus |

## Pipeline

```text
STEP 0: KLARIFIKASI   → mode input, topik/kata kunci, jumlah, kolom, filter, bahasa, format ekspor
STEP 1: AKUISISI      → kumpulkan paper (search ATAU folder ATAU hybrid) + dedup + verifikasi
STEP 2: EKSTRAKSI     → baca abstract/teks tiap paper, isi setiap kolom + kumpulkan metadata biblio
STEP 3: TABEL         → simpan papers.json (data terstruktur) → render markdown + export 5 format
STEP 4: TRIASE        → laporan statistik + verifikasi DOI + quality gate
```

Setiap step punya quality gate; minta konfirmasi user sebelum langkah besar.

---

## STEP 0 — Klarifikasi

Tanyakan parameter berikut (minimalkan bila konteks sudah jelas):

| Parameter | Opsi | Default |
|-----------|------|---------|
| Mode input | Search / Folder / Hybrid | sesuai permintaan |
| Topik / kata kunci | wajib (untuk Search/Hybrid) | — |
| Jumlah paper target | angka | 10–15 (search), seluruh file (folder) |
| Kolom table | default 12 kolom (literature review matrix) + kolom custom | default |
| Makna kolom "Gaps" | `gap yang di-address paper` vs `gap/kelangkaan yang bisa jadi riset baru` | gap yang di-address paper (Limitations sudah punya kolom sendiri) |
| Rentang tahun | bebas | 5 tahun terakhir (search) |
| Filter kualitas jurnal | Scopus Quartile / peer-reviewed saja / tanpa filter | tanpa filter tapi tetap tag sumber |
| Bahasa paper | Indonesia / Inggris / semua | Inggris |
| Format output tabel | Markdown | Markdown |
| Format ekspor | CSV / Excel (XLSX) / BibTeX (BIB) / XML (EndNote) / RIS / semua | Bergantung permintaan (default: MD saja; "export semua" → 5 format) |
| Folder target | wajib (untuk Folder/Hybrid) | — |

**Kolom default (literature review matrix** — blok sitasi dulu, lalu blok ekstraksi; user boleh menghapus/menambah):

| # | Kolom | Definisi |
|---|-------|----------|
| 1 | Title & Authors | Judul + penulis (format sitasi ringkas; > 6 penulis → `Penulis1 et al.`) |
| 2 | Journal | Nama jurnal |
| 3 | Year | Tahun terbit |
| 4 | Purpose | Tujuan penelitian, 1 kalimat |
| 5 | Method (Variables/Samples) | Desain, IV/DV, n=, sampel, instrumen, analisis |
| 6 | Key Findings | Hasil/findings utama (angka kunci jika ada) |
| 7 | Limitations | Keterbatasan yang diakui penulis |
| 8 | Gaps | Research gap yang di-address paper (bisa diganti maknanya di Step 0) |
| 9 | Theory Used | Teori/kerangka konseptual |
| 10 | Novelty/Contribution | Klaim kebaruan + kontribusi |
| 11 | Future Studies | Saran penelitian lanjutan |
| 12 | DOI & Publisher | DOI + penerbit |

**Kolom custom** (fitur "Add Columns"): user dapat menambah kolom apa saja, mis.
`Relevance (0–10)`, `Citations`, `Sampling Method`, `Instruments`, `Recommendations`. Kolom custom
diisi dari isi paper, atau dari pertanyaan tambahan yang diminta user. Tambahkan ke tabel & JSON,
jangan dihapus kolom default tanpa izin.

---

## STEP 1 — Akuisisi Paper

> Load `references/search-sources.md` untuk pencarian online.
> Load `references/extracting-papers.md` untuk membaca folder PDF/LaTeX.

### Mode A — Search
1. Pecah topik menjadi 3–5 konsep inti → buat 8–15 kombinasi kata kunci.
2. Cari dengan kata kunci di OpenAlex API dulu (gratis), lalu Semantic Scholar / arXiv bila perlu, atau
   gunakan web search tools yang tersedia di lingkungan agent.
3. Kumpulkan 1.5× jumlah target sebagai kandidat; skor relevansi 0–10 dari judul+abstract.
4. Pertahankan kandidat dengan relevansi ≥ 7/10 hingga mencapai jumlah target.
5. Ambil `doi`, `title`, `abstract`, `authors`, `year`, `journal/publisher` dari metadata API.

### Mode B — Folder
1. Scan folder target (mendukung rekursif).
2. Pisahkan: file `*.pdf` (perlu ekstraksi teks, lihat `scripts/extract_text.sh`) vs `*.tex` (baca langsung).
3. Untuk PDF, ekstrak teks; cara cepat tanpa Script: gunakan `pdftotext <file> -` (poppler) atau `python -c "import pypdf..."` bila tersedia.
4. Dari teks, ambil abstract/intro/method/conclusion sesuai panduan `references/extracting-papers.md`.

### Mode C — Hybrid
Gabung hasil keduanya, dedup berdasarkan DOI (atau judul, bila DOI tidak ada). Kandidat yang sama
muncul sekali; prefer data dari file lokal (lebih lengkap) atas metadata search.

### Dedup & Verifikasi
- Dedup berdasarkan DOI; tanpa DOI, berdasarkan judul normalisasi (lowercase, hilangkan tanda baca).
- Setiap DOI harus dapat di-resolve (`https://doi.org/<doi>`). Yang gagal → tandai `UNVERIFIED`.
- Jika paper hanya disebut tapi tidak ada bukti keberadaan (DOI/title di sumber terverifikasi) → **JANGAN** masukkan.

### Output Step 1
```
candidate_papers.md   — FILE KERJA INTERNAL (bukan output utama)
                         daftar kandidat + skor relevansi + status verifikasi DOI
```

> ⚠️ **JANGAN berhenti di Step 1.** Daftar kandidat hanyalah *working file internal*. Output yang
> wajib diserahkan ke user adalah **tabel penuh per-paper** (literature_table.md + papers.json + export),
> di mana **setiap paper = satu baris** dengan semua kolom review terisi. Recap/count hanya pelengkap di akhir.

### Quality Gate 1
- [ ] Jumlah kandidat ≥ jumlah target (atau disepakati)
- [ ] Setiap baris dilengkapi DOI atau file lokal (bukti keberadaan)
- [ ] DOI gagal diverifikasi sudah ditandai `UNVERIFIED`
- [ ] **Izin sekali di awal sudah cukup** — jangan minta konfirmasi per-candidate; setelah scope jelas
      (topik, jumlah, kolom), langsung ekstraksi penuh semua paper yang lolos.

---

## STEP 2 — Ekstraksi Per Paper

> **Mandat utama skill ini:** bangun tabel penuh di mana **setiap paper = satu baris** dan **setiap
> kolom review terisi** (atau `—` bila data tidak tersedia). Jangan mengganti output ini dengan tabel
> rekap (jumlah paper, summary gabungan, atau daftar kandidat).

Untuk tiap paper, isi semua kolom. Aturan ringkas:

### Cara Mengisi Sel (Meniru Data Extraction)

Sel BUKAN frasa pendek, melainkan **2–5 kalimat lengkap** yang memuat detail paper, dan **setiap
kalimat/klaim diberi penanda sumber** (provenance) berupa kode bagian + nomor paragraf di belakangnya:

```
Contoh (kolom Method, Mode Folder):
Penelitian menggunakan analisis komparatif statistik untuk membandingkan efektivitas
metode Kanban dan Scrum pada proyek Agile berbiaya dan berjadwal tetap [M-2].
Pengumpulan data memakai convenience sampling dari ahli manajemen proyek Agile
berpengalaman ≥ 1 tahun [M-5][M-6]. Analisis data melalui Confirmatory Component
Analysis (CCA) dan uji hipotesis korelasi intra-variabel, serta reliabilitas dengan CR
dan Cronbach [M-7]. Studi mengecualikan batasan jadwal dan biaya, fokus pada sumber
daya, ruang lingkup, dan risiko [M-8].
```

**Kode penanda (legend)**: | Kode | Bagian paper | (AB = Abstract, I = Introduction, M = Method, R = Results, D = Discussion, L = Limitations, F = Future Work, C = Conclusion). `[M-2]` = Method paragraf 2; `[D-1][D-2]` = klaim dari gabungan paragraf. Selipkan penanda tepat setelah kalimat sumbernya.

- **Mode Folder/LaTeX** (teks lengkap): penanda = bagian + nomor paragraf nyata yang Anda baca.
- **Mode Search** (hanya abstract/metadata): penanda `[AB]`; konten sel otomatis lebih ringkas karena
  keterbatasan sumber — tulis kolom lain yang tak tersedia dengan `—` (bukan mengarang detail).
- Jika beberapa kalimat berasal dari bagian sama, ulangi penanda di tiap kalimat.

Aturan per kolom:

| Kolom | Sumber di paper | Isi sel yang diharapkan |
|-------|-----------------|-------------------------|
| Title & Authors | Halaman judul / metadata | Judul + penulis; > 6 penulis → `Penulis1 et al.` |
| Journal / Year | Halaman judul, header LaTeX, metadata | Nama jurnal / tahun |
| Purpose | Abstract & Intro | 1–2 kalimat tujuan + `[AB]` / `[I-n]` |
| Method (Variables/Samples) | Method section | Desain; **sampel (ukuran, teknik, komposisi)**; variabel; instrumen; analisis — tiap klaim ber-penanda `[M-n]` |
| Key Findings | Results / Abstract | Hasil utama + angka kunci (efek, koefisien, p-value, n) — ber-penanda `[R-n]` |
| Limitations | Discussion / Limitations | Tiap keterbatasan 1 kalimat + `[D-n]` / `[L-n]` |
| Gaps | Intro / pembahasan | Gap yang di-address paper + `[I-n]` |
| Theory Used | Intro / Lit Review | Teori + dasar penggunaannya + `[I-n]` |
| Novelty/Contribution | Intro & Conclusion | Klaim kontribusi + `[I-n]` / `[C-n]` |
| Future Studies | Future Work / Conclusion | **Semua** rekomendasi lanjutan, masing-masing + `[F-n]` / `[C-n]` |
| DOI & Publisher | Metadata / file | `DOI: 10.xxxx/... \| Penerbit` |

**Metadata biblio** (untuk export BibTeX/RIS/XML — kumpulkan bila tersedia dari metadata API/file):
`authors` (daftar, format `Surname, Given`), `title`, `year`, `journal`, `volume`, `issue`, `pages`,
`doi`, `publisher`, `url`, `abstract`, `keywords`. Field yang tidak ada → string kosong (bukan `—`)
di JSON, agar tidak ikut ter-export ke sitasi.

1. Minim baca: **Abstract** → **Intro** → **Method** → **Results** → **Conclusion/Future Work**.
2. Untuk paper yang tidak terbaca penuh (PDF hasil OCR buruk): isi dari abstract saja, tandai field kosong `—`.
3. Jika abstract tidak tersedia di metadata API maupun file → tulis `—`, JANGAN mengarang.

### Output Step 2
Sementara hasil ekstraksi disimpan sebagai file draft (mis. `extraction_draft.md`) atau langsung
menjadi baris tabel — ikuti preferensi user; untuk jumlah besar (> 10 paper) sarankan draft per paper dulu.

---

## STEP 3 — Susun Tabel & Export

> Load `references/table-builder.md` untuk detail render & export.
> Gunakan template `templates/paper_review_table_template.md`.

Workflow ini menghasilkan **satu sumber data → banyak format** (data extraction):

1. **Bangun `papers.json`** dulu — data terstruktur per paper (metadata biblio + nilai tiap kolom).
   Ini adalah *master data*; seluruh format diturunkan dari sini.
   Format skema JSON ada di `scripts/export_formats.py` dan `references/table-builder.md`.
2. **Render markdown** dari JSON: tabel GitHub-flavored, satu baris per paper.
3. **Export** sesuai format yang diminta user:
   ```
   python3 scripts/export_formats.py papers.json \
       --formats csv,xlsx,bib,xml,ris --out <folderkeluaran>
   ```
   - `.csv` — selaras untuk Excel/Google Sheets (UTF-8 with BOM)
   - `.xlsx` — Excel: sheet `Papers` (header terformat + autofilter) + sheet `Metadata`
   - `.bib` — BibTeX `@article` siap import ke Zotero/JabRef/Overleaf
   - `.xml` — EndNote XML (`<records><record>`) siap import ke EndNote/Zotero
   - `.ris` — RIS `JOUR` siap import ke Zotero/Mendeley/EndNote
4. Tambahkan **Metadata Pencarian** di atas tabel dan **Legenda Penanda Sumber (provenance)** di bawah tabel:

   ```markdown
   **Legenda — kode bagian paper:**
   | AB | I | M | R | D | L | C | F |
   |----|---|---|---|---|---|---|---|
   | Abstract | Introduction | Method | Results | Discussion | Limitations | Conclusion | Future Work |
   ```
   Penanda seperti `[M-2]` = klaim diambil dari bagian Method, paragraf 2. Ini yang membuat hasil
   **dapat ditelusuri ke bagian paper** (penandaan kode bagian + nomor paragraf, seperti nomor kutipan kecil).

> Jika `openpyxl` belum terpasang untuk XLSX: jalankan `pip3 install openpyxl`, atau output CSV
> sebagai gantinya dan beri tahu user.

### Output Step 3
```
📋 OUTPUT UTAMA (wajib):
  literature_table.md  — tabel review final: setiap paper 1 baris, semua kolom review terisi
  papers.json          — master data terstruktur (metadata biblio + nilai kolom)
🗂 EXPORT (sesuai permintaan):
  literature_table.csv | .xlsx | .bib | .xml | .ris
```

> Pastikan tabel di atas berisi **setiap hasil review per paper** (bukan ringkasan antar paper).
> Jika user hanya melihat recap (count / daftar kandidat), itu artinya Anda berhenti terlalu cepat —
> lanjutkan hingga tabel penuh per-paper selesai.

---

## STEP 4 — Triase Ringkas & Quality Gate

> Ringkasan ini **pelengkap di akhir** (bagian bawah literature_table.md), BUKAN pengganti tabel penuh.

### Laporan Triase
```
Dari [X] kandidat:
- Lolos relevansi ≥ 7/10 : [Y]
- Mode search : [a] | mode folder : [b] | hybrid : [c]
- DOI terverifikasi : [d] | UNVERIFIED : [e]
- Dibuang (relevansi < 7 / duplikat / tidak terbukti) : [f]
```

### Quality Gate Akhir
- [ ] Semua kolom default terisi (atau `—` bila data tidak tersedia) — **tidak boleh sel kosong misterius**
- [ ] Kolom custom yang disepakati terisi
- [ ] Tidak ada referensi/DOI yang diimajinasikan
- [ ] Verifikasi kilat: spot-check 2–3 DOI dapat di-resolve
- [ ] User setuju hasil akhir

---

## Alur Pemakaian Cepat

| Permintaan | Action |
|-----------|--------|
| "Cari 15 paper tentang X dan buatkan tabel" | Mode A → **langsung tabel penuh per-paper** (literature_table.md) |
| "Review semua paper di folder [path]" | Mode B → semua file → **tabel penuh per-paper** |
| "Tabel dengan kolom tambahan Findings" | Step 0: tambah kolom custom `Findings` |
| "Kombinasi search + folder saya" | Mode C, dedup DOI |
| "Export ke CSV/Excel/BibTeX/XML/RIS" | Step 3: bangun papers.json → `export_formats.py` |
| "Export semua 5 format" | `--formats csv,xlsx,bib,xml,ris` |
| "Tabel dengan makna Gaps = gap riset baru" | Step 0: ubah definisi kolom Gaps |

## Aturan Penting (Selalu Berlaku)

0. **Output utama = tabel penuh per-paper.** Setiap paper = satu baris, semua kolom review terisi
   (atau `—`). Recap count / daftar kandidat hanya pelengkap di akhir — JANGAN menyerahkannya sebagai hasil.
1. **Jangan mengarang paper.** Setiap baris wajib punya DOI (dapat di-resolve) atau file lokal yang dibaca.
   Ragu → tandai `UNVERIFIED — cek manual`.
2. **Jangan mengarang isi kolom.** Field tidak tersedia → `—`; inferensi → tandai `(diringkas)`.
3. **Ambil klaim, bukan opini.** Kolom Novelty/Gaps diisi dari pernyataan paper, bukan penilaian agent.
4. **Human-in-the-loop**: agent mengusulkan tabel, user memutuskan kolom & jumlah.
5. **Simpan artefak sebagai file** (markdown/csv) di folder kerja user, jangan hanya di chat.
6. **Reproducible**: sertakan tanggal search + kata kunci + kombinasi keywords di Metadata Pencarian.

## Referensi Internal

| File | Gunakan untuk |
|------|---------------|
| [references/search-sources.md](references/search-sources.md) | Pencarian online (OpenAlex/Semantic Scholar/arXiv) |
| [references/extracting-papers.md](references/extracting-papers.md) | Membaca folder PDF/LaTeX + per-field extraction |
| [references/table-builder.md](references/table-builder.md) | Skema papers.json, render tabel, export 5 format |
| [templates/paper_review_table_template.md](templates/paper_review_table_template.md) | Template tabel review |
| [scripts/extract_text.sh](scripts/extract_text.sh) | Ekstraksi teks PDF dalam folder |
| [scripts/export_formats.py](scripts/export_formats.py) | Export CSV/XLSX/BIB/XML/RIS dari papers.json |

## Attribution

Subset dari **bimajanuri/academic-writing-skill** (pencarian literatur + literature matrix),
yang mereferensikan metodologi dari Master-cai/Research-Paper-Writing-Skills, SNL-UCSB/paper-writing-skill,
dan WenyuChiou/ai-research-skills (literature triage matrix). Struktur tabel & daftar format ekspor
meniru fitur **Literature Review / Data Extraction** pada platform reference-manager AI
(synthesis matrix + CSV/XLSX/BIB/XML/RIS).
Lihat README academic-writing-skill untuk detail.

## Platform Note

Format Agent Skills (SKILL.md) portabel ke OpenCode (`~/.config/opencode/skills/`),
Claude Code (`~/.claude/skills/`), dan platform lain dengan menyalin folder ini.