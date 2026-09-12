# Search Sources — Pencarian Literatur Online

Panduan pencarian paper akademik untuk **Mode A (Search)** dan **Mode C (Hybrid)** pada skill paper-review.
Dukungan **filter Scopus Quartile (Q1–Q4)**, snowballing, dan literatur fondasi, di samping
**metode review folder lokal** (lihat `extracting-papers.md`).

## 1. Klarifikasi Awal

Sebelum mencari (selain Step 0 di SKILL.md), pastikan parameter berikut sudah jelas dari user:

| Parameter | Opsi | Default |
|-----------|------|---------|
| Topik / kata kunci | wajib diisi | — |
| Filter Scopus Quartile | Q1 / Q2 / Q3 / Q4 / tanpa filter | Tanpa filter (tapi tetap tag quartile) |
| Rentang tahun | bebas | 5 tahun terakhir |
| Jumlah target | bebas | 10–15 (search), seluruh file (folder) |
| Bahasa paper | Indonesia / Inggris / semua | Inggris |
| Sumber | OpenAlex / Semantic Scholar / arXiv / semua | Semua (OpenAlex dulu) |
| Jenis dokumen | artikel riset / review / semua | Artikel riset + review |
| Folder target | wajib (untuk Folder/Hybrid) | — |

## 2. Prioritas Sumber (Tanpa API Key)

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
   kombinasi keyword, mengambil metadata dari DOI, memverifikasi quartile, atau mengambil halaman jurnal.

Catatan: bila agent lingkungan punya tools web, gunakan tools tersebut; API di atas sebagai sumber
kandidat DOI/referensi yang kemudian **diverifikasi**.

## 3. Strategi Pencarian Multi-Tahap

### Round 1 — Pencarian Langsung (Literatur Primer)
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
4. Kumpulkan kandidat hingga ≥ 1.5× jumlah target (30–50 kandidat untuk target besar).
5. Skor relevansi 0–10 dari judul + abstract; pertahankan yang ≥ 7/10.

### Round 2 — Snowballing (bila jumlah kurang)
- **Backward**: telusuri referensi yang dikutip di dalam paper kunci → verifikasi DOI → tambahkan.
- **Forward**: paper yang mensitasi paper kunci → `filter=cites:<openalex_id>` di OpenAlex,
  atau daftar "cited by" Semantic Scholar.
- Kumpulkan **5–15 paper tambahan** dari jaringan sitasi.

### Round 3 — Literatur Klasik / Fondasi (opsional)
- Identifikasi paper highly-cited (>100 sitasi) yang relevan → **2–5 paper fondasi** untuk konteks
  (cocok untuk kolom Theory Used).
- Rentang tahun **dilonggarkan** untuk fondasi; tetap tag quartile bila dari jurnal.

## 4. Metadata yang Diambil per Paper

Kumpulkan minimal:
- `doi`, `title`, `year`, `authors` (format `Penulis1, Penulis2, & Penulis3`), `journal/publisher`, `abstract`.

Jika abstract tidak tersedia di metadata, coba `abstract_inverted_index` OpenAlex untuk merekonstruksi;
bila tetap kosong → field yang bergantung abstract diisi `—`.

## 5. Filter Scopus Quartile (Q1–Q4)

### Prinsip
- **Hanya Scopus denominator.** Quartile mengacu pada **CiteScore/SJR quartile** Scopus (Q1, Q2, Q3, Q4),
  bukan SINTA/ARJUNA/Lainnya.
- Data quartile dari **Scimago Journal Rank (SJR)** di scimagojr.com atau metadata yang dapat dipercaya.
- Sarankan **kolom `Quartile`** pada tabel (bisa jadi kolom custom, mis. `Quartile` / `Source Quartile`).

### Verifikasi Quartile per Jurnal
1. Ambil nama jurnal + ISSN dari metadata paper (OpenAlex `primary_location.source`).
2. Tentukan quartile dari salah satu:
   - Fetch halaman scimagojr.com (jika tools web tersedia)
   - Basis pengetahuan yang yakin (Nature, Cell, IEEE TPAMI, dll.)
   - Perkiraan → label **`ESTIMATED`**
3. Pemetaan quartile:
   - **Q1**: CiteScore ranking atas 25% bidang
   - **Q2**: persentil 25–50%
   - **Q3**: persentil 50–75%
   - **Q4**: persentil 75–100% (atau jurnal tidak terindeks Scopus → `OUT`)

Tidak dapat diverifikasi → tag `[quartile: UNVERIFIED]`.

### Skema Filter (berlaku di matrix/tabel)

| Mode | Perilaku |
|------|----------|
| **Tanpa filter** | Semua paper lolos relevansi masuk tabel; kolom Quartile tetap diisi (label jurnal + quartile) |
| **Filter Q1** | Hanya jurnal Q1 yang masuk; Q2–Q4 dan non-Scopus dibuang |
| **Filter Q1–Q2** | Quartile Q1 dan Q2 masuk; Q3, Q4, non-Scopus dibuang |
| **Filter Q3–Q4 dsb.** | analog |
| **Peer-reviewed saja** | Buang preprint / tanpa metadata penerbit |

**Jurnal non-Scopus** (arXiv preprint, paper konferensi non-Scopus, dsb.): masukkan ke **tabel terpisah**
berlabel `[non-Scopus]`, supaya tidak menggabungkan standar — tanyakan ke user apakah perlu disertakan.

### Laporan Penyaringan (di laporan triase akhir)
```
Dari X kandidat:
- Lolos relevansi ≥ 7/10 : Y paper
- Scopus Q1 : a | Q2 : b | Q3 : c | Q4 : d
- Non-Scopus : e
- Dibuang (relevansi < 7 / duplikat / tidak terbukti / di luar filter quartile) : f
```

## 6. Anti-Hallucination (Wajib)

1. Setiap DOI wajib diverifikasi dapat di-resolve (`https://doi.org/<doi>`). Gagal → `UNVERIFIED`.
2. Referensi yang disebut tanpa bukti DOI/keberadaan → JANGAN masuk tabel; beri tahu user.
3. Jangan menebak nama jurnal, volume, halaman, atau tahun.
4. Metadata tidak lengkap → isi kolom yang kurang dengan `—`; quartile tak terverifikasi → `UNVERIFIED`.

## 7. Output

Simpan daftar kandidat sebagai:
```
candidate_papers.md  — daftar kandidat + mode + skor relevansi + status quartile + status verifikasi DOI
```
Lanjut ke `extracting-papers.md` untuk ekstraksi per-field (termasuk cara baca folder PDF/LaTeX),
lalu `table-builder.md` untuk render.