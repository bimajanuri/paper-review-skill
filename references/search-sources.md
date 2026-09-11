# Search Sources — Pencarian Literatur Online

Panduan pencarian paper akademik untuk **Mode A (Search)** dan **Mode C (Hybrid)** pada skill paper-review.

## 1. Prioritas Sumber (Tanpa API Key)

1. **OpenAlex API** (gratis, paling lengkap, mencakup jurnal terindeks Scopus)
   ```
   GET https://api.openalex.org/works?search=KATA+KUNCI&filter=from_publication_date:YYYY-MM-DD,type:article|review
   ```
   - Tambahkan `&mailto=email@example.com` untuk polite pool (rate limit lebih tinggi).
   - Response mencakup `doi`, `title`, `authorships`, `publication_date`, `biblio`, dan
     `primary_location.source` (nama jurnal + issn).
2. **Semantic Scholar API** (gratis)
   ```
   GET https://api.semanticscholar.org/graph/v1/paper/search?query=KATA+KUNCI&fields=title,authors,year,externalIds,abstract,venue&limit=20
   ```
   - Kaya data abstract (untuk kolom Purpose/Method ringkas).
3. **arXiv API** (preprint CS/fisika) — opsional; beri label `non-Scopus` / UNVERIFIED untuk quartile
   ```
   GET http://export.arxiv.org/api/query?search_query=all:KATA+KUNCI&max_results=20
   ```
4. **Web search / fetch tools** di lingkungan agent (websearch/webfetch) — gunakan untuk menambah
   kombinasi keyword, mengambil metadata dari DOI, atau memverifikasi halaman jurnal.

## 2. Strategi Multi-Tahap

### Round 1 — Pencarian Langsung
1. Pecah topik menjadi 3–5 konsep inti.
2. Buat 8–15 kombinasi kata kunci: `konsep1 + konsep2`, `konsep + metode`,
   sinonim/varian disiplin. Contoh untuk "pengaruh medsos terhadap akademik":
   ```
   - "social media" AND "academic performance"
   - "social media usage" AND "student"
   - "screen time" AND "learning outcomes"
   - "media multitasking" AND "grade point average"
   - sinonim: "digital distraction", "technology use"
   ```
3. Cari tiap kombinasi di OpenAlex / Semantic Scholar.
4. Kumpulkan kandidat hingga ≥ 1.5× jumlah target.
5. Skor relevansi 0–10 dari judul + abstract; pertahankan yang ≥ 7/10.

### Round 2 — Snowballing (bila jumlah kurang)
- **Backward**: telusuri referensi di dalam paper kunci → verifikasi DOI → tambahkan.
- **Forward**: paper yang mensitasi paper kunci → `filter=cites:<openalex_id>` di OpenAlex,
  atau daftar "cited by" Semantic Scholar.

### Round 3 — Literatur Fondasi (opsional)
- Paper highly-cited (>100 sitasi) yang relevan → untuk kolom Theory Used / konteks.
- Rentang tahun dilonggarkan untuk fondasi.

## 3. Metadata yang Diambil per Paper

Kumpulkan minimal:
- `doi`, `title`, `year`, `authors` (format `Penulis1, Penulis2, & Penulis3`), `journal/publisher`, `abstract`.

Jika abstract tidak tersedia di metadata, coba `abstract_inverted_index` OpenAlex untuk merekonstruksi;
bila tetap kosong → field yang bergantung abstract diisi `—`.

## 4. Filter Kualitas Jurnal (Opsional)

| Mode | Perilaku |
|------|----------|
| **Tanpa filter** | Semua paper lolos relevansi masuk; kolom Source tetap isi jurnal + tahun |
| **Peer-reviewed saja** | Buang preprint/tanpa metadata penerbit |
| **Scopus Quartile (Q1–Q4)** | Tambahkan kolom `Quartile`. Verifikasi via Scopus SJR (scimagojr.com) atau metadata yang dapat dipercaya; tidak yakin → `Q? [UNVERIFIED]`; arXiv/preprint → `non-Scopus` |

Prinsip: quartile mengacu pada **CiteScore/SJR Scopus**, bukan SINTA/ARJUNA. Jurnal non-Scopus
bisa dimasukkan di tabel terpisah berlabel `[non-Scopus]` bila user menginginkannya.

## 5. Anti-Hallucination (Wajib)

1. Setiap DOI wajib diverifikasi dapat di-resolve (`https://doi.org/<doi>`). Gagal → `UNVERIFIED`.
2. Referensi yang disebut tanpa bukti DOI/keberadaan → JANGAN masuk tabel; beri tahu user.
3. Jangan menebak nama jurnal, volume, halaman, atau tahun.
4. Metadata tidak lengkap → isi kolom yang kurang dengan `—`.

## 6. Output

Simpan daftar kandidat sebagai:
```
candidate_papers.md  — daftar kandidat + mode + skor relevansi + status verifikasi DOI
```
Lanjut ke `extracting-papers.md` untuk ekstraksi per-field, lalu `table-builder.md` untuk render.