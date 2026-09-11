---
name: paper-review
description: |
  Menghasilkan tabel review literatur akademik dari (a) pencarian online berdasarkan topik + kata kunci + jumlah target, atau (b) folder lokal berisi paper berformat PDF/LaTeX, atau (c) kombinasi keduanya. Output berupa tabel dengan kolom Authors/Title, Purpose, Gaps, Method (Variables/Samples), Theory Used, Novelty/Contribution, Future Studies, Source (DOI & Publisher) — plus kolom custom apa pun yang diminta. Generates a literature review table from online search or a local folder of PDF/LaTeX papers. Trigger: "literature review", "tabel review paper", "tabel literatur", "review paper di folder ini", "cari paper tentang X sebanyak N", "literature matrix", "synthesize papers", "review jurnal", "subset of academic-writing-skill".
---

# Paper Review — Review & Sintesis Literatur

Skill ini membuat **tabel review** terstruktur dari paper akademik. Merupakan subset terfokus dari
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
STEP 0: KLARIFIKASI   → mode input, topik/kata kunci, jumlah, kolom, filter, bahasa, format output
STEP 1: AKUISISI      → kumpulkan paper (search ATAU folder ATAU hybrid) + dedup + verifikasi
STEP 2: EKSTRAKSI     → baca abstract/teks tiap paper, isi setiap kolom
STEP 3: TABEL         → render tabel markdown/CSV dengan kolom default + custom
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
| Kolom table | default 8 kolom + kolom custom | default |
| Makna kolom "Gaps" | `gap yang di-address paper` vs `keterbatasan (limitations) paper` | gap yang di-address paper |
| Rentang tahun | bebas | 5 tahun terakhir (search) |
| Filter kualitas jurnal | Scopus Quartile / peer-reviewed saja / tanpa filter | tanpa filter tapi tetap tag sumber |
| Bahasa paper | Indonesia / Inggris / semua | Inggris |
| Format output | Markdown / CSV / keduanya | Markdown |
| Folder target | wajib (untuk Folder/Hybrid) | — |

**Kolom default** (selalu tersedia, kecuali user menghapus):

| # | Kolom | Definisi |
|---|-------|----------|
| 1 | Authors/Title | Nama penulis (format sitasi ringkas) + judul paper |
| 2 | Purpose | Tujuan penelitian, 1 kalimat |
| 3 | Gaps | Research gap yang di-address / limitations (sesuai kesepakatan Step 0) |
| 4 | Method (Variables/Samples) | Desain, IV/DV, n=, sampel, instrumen, analisis |
| 5 | Theory Used | Teori/kerangka konseptual |
| 6 | Novelty/Contribution | Klaim kebaruan + kontribusi |
| 7 | Future Studies | Saran penelitian lanjutan |
| 8 | Source (DOI & Publisher) | DOI + jurnal/penerbit (+ tahun) |

**Kolom custom**: user dapat menambah kolom apa saja, mis. `Relevance (0–10)`, `Findings`, `Quartile`,
`Screenshot Evidence`, `Referensi Lain yang Disarankan`. Kolom custom diisi dari isi paper, atau dari
pertanyaan tambahan yang diminta user. Tambahkan ke template tabel, jangan dihapus kolom default tanpa izin.

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
candidate_papers.md   — daftar kandidat + mode sumber + skor relevansi + status verifikasi DOI
```

### Quality Gate 1
- [ ] Jumlah kandidat ≥ jumlah target (atau disepakati)
- [ ] Setiap baris dilengkapi DOI atau file lokal (bukti keberadaan)
- [ ] DOI gagal diverifikasi sudah ditandai `UNVERIFIED`
- [ ] User setuju daftar paper sebelum ekstraksi penuh

---

## STEP 2 — Ekstraksi Per Paper

Untuk tiap paper, isi semua kolom. Aturan ringkas:

| Kolom | Sumber di paper | Catatan |
|-------|-----------------|---------|
| Authors/Title | Halaman judul / metadata | > 6 penulis → `Penulis1 et al.` |
| Purpose | Abstract & Intro | 1 kalimat; ringkasan inferensi → tandai `(diringkas)` |
| Gaps | Intro (gap yang di-address) / Discussion-Limitation | sesuai kesepakatan Step 0 |
| Method | Method section | Desain; IV/DV; n=; sampel; instrumen; analisis |
| Theory Used | Intro / Lit Review | Tidak disebut → `Tidak disebut eksplisit` |
| Novelty/Contribution | Intro & Conclusion | Ambil klaim paper, jangan opini sendiri |
| Future Studies | Future Work / Conclusion | Tidak ada → `—` |
| Source (DOI & Publisher) | Metadata / file | `DOI: 10.xxxx/... \| Jurnal \| Tahun` |

1. Minim baca: **Abstract** → **Intro** → **Method** → **Conclusion/Future Work**.
2. Untuk paper yang tidak terbaca penuh (PDF hasil OCR buruk): isi dari abstract saja, tandai field kosong `—`.
3. Jika abstract tidak tersedia di metadata API maupun file → tulis `—`, JANGAN mengarang.

### Output Step 2
Sementara hasil ekstraksi disimpan sebagai file draft (mis. `extraction_draft.md`) atau langsung
menjadi baris tabel — ikuti preferensi user; untuk jumlah besar (> 10 paper) sarankan draft per paper dulu.

---

## STEP 3 — Susun Tabel

> Load `references/table-builder.md` untuk detail render & kolom custom.
> Gunakan template `templates/paper_review_table_template.md`.

1. Susun header sesuai kolom yang disepakati (default + custom). Urutan kolom bebas diubah user.
2. Isi satu baris per paper dengan konten ekstraksi Step 2.
3. Render:
   - **Markdown**: tabel GitHub-flavored.
   - **CSV** (opsional): keluwesan standar, kutip nilai berisi koma dengan `"..."`.
4. Tambahkan **Metadata Pencarian** di atas tabel (topik, kata kunci, mode, sumber, jumlah, tanggal).
5. Tambahkan **Legenda** di bawah tabel (makna `—`, `(diringkas)`, `UNVERIFIED`).

### Output Step 3
```
literature_table.md   — tabel review final (markdown)
literature_table.csv  — versi CSV bila diminta
```

---

## STEP 4 — Triase & Quality Gate

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
| "Cari 15 paper tentang X dan buatkan tabel" | Mode A, default kolom → literature_table.md |
| "Review semua paper di folder [path]" | Mode B, semua file → literature_table.md |
| "Tabel dengan kolom tambahan Findings" | Step 0: tambah kolom custom `Findings` |
| "Kombinasi search + folder saya" | Mode C, dedup DOI |
| "Ekspor ke CSV" | Step 3: output `literature_table.csv` |
| "Tabel dengan makna Gaps = limitations" | Step 0: ubah definisi kolom Gaps |

## Aturan Penting (Selalu Berlaku)

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
| [references/table-builder.md](references/table-builder.md) | Render tabel, kolom custom, format MD/CSV |
| [templates/paper_review_table_template.md](templates/paper_review_table_template.md) | Template tabel review |
| [scripts/extract_text.sh](scripts/extract_text.sh) | Ekstraksi teks PDF dalam folder |

## Attribution

Subset dari **bimajanuri/academic-writing-skill** (pencarian literatur + literature matrix),
yang mereferensikan metodologi dari Master-cai/Research-Paper-Writing-Skills, SNL-UCSB/paper-writing-skill,
dan WenyuChiou/ai-research-skills (literature triage matrix). Lihat README academic-writing-skill untuk detail.

## Platform Note

Format Agent Skills (SKILL.md) portabel ke OpenCode (`~/.config/opencode/skills/`),
Claude Code (`~/.claude/skills/`), dan platform lain dengan menyalin folder ini.