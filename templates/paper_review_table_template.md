# Template Tabel Review Paper (Literature Review Matrix)

> ⚠️ **Output UTAMA** adalah tabel penuh di bawah ini — **setiap paper = satu baris**, semua kolom
> review terisi. Bagian Metadata/Triase/Legenda adalah pelengkap, bukan pengganti tabel.

Salin struktur ini untuk output tabel. **Blok sitasi + blok ekstraksi** (literature review matrix)
+ ruang kolom custom. Isi `—` bila data tidak tersedia di paper/sumber.

> **Isi sel:** komprehensif — masing-masing kolom ekstraksi berisi **2–5 kalimat lengkap** dengan
> detail paper (bukan frasa singkat), dan tiap kalimat diberi **penanda sumber `[KODE-n]`** di ujungnya
> (contoh `[M-2]` = Method paragraf 2; kode bagian: AB/I/M/R/D/L/C/F). Lihat contoh real di bawah
> placeholder sel `[METHOD]` dan `[FUTURE]` — hasilnya harus setara detailnya.

## Metadata Pencarian

- **Mode**: [Search / Folder / Hybrid]
- **Topik**: [topik penelitian]
- **Query/kata kunci**: [keyword + kombinasi yang dipakai]
- **Jumlah target**: [N] | **Jumlah baris**: [M]
- **Rentang tahun**: [YYYY–YYYY] | **Tanggal**: [YYYY-MM-DD]
- **Sumber**: [OpenAlex / Semantic Scholar / arXiv / Folder: <path> / kombinasi]

## Tabel Review

| No | Title & Authors | Journal | Year | Purpose | Method (Variables/Samples) | Key Findings | Limitations | Gaps (yang di-address) | Theory Used | Novelty/Contribution | Future Studies | DOI & Publisher |
|----|-----------------|---------|------|---------|---------------------------|--------------|-------------|------------------------|-------------|----------------------|----------------|-----------------|
| 1  | [Penulis (Tahun)] — "[Judul]" | [Jurnal] | [Tahun] | [Tujuan 1–2 kalimat] [I-1] | **[METHOD]** Desain [M-2]. Sampling [M-5]. Analisis [M-7]. Pengecualian [M-8]. | [Hasil utama + angka kunci] [R-1][R-2] | [Keterbatasan 1] [D-1]. [Keterbatasan 2] [D-2]. | [Gap yang di-address] [I-2] | [Teori] [I-3] | [Klaim kontribusi] [C-1] | **[FUTURE]** Saran 1 [F-1]. Saran 2 [F-2]. | DOI: 10.xxxx/... \| [Penerbit] |
| 2  | | | | | | | | | | | | |

**Contoh real — sel Method (komprehensif, dengan penanda sumber):**
Penelitian menggunakan analisis komparatif statistik untuk membandingkan efektivitas metode Kanban dan Scrum dalam pengembangan perangkat lunak Agile, dengan fokus pada proyek yang memiliki biaya tetap dan jadwal tetap [M-2]. Metode pengumpulan data melibatkan penggunaan sampel yang nyaman dari para ahli di bidang manajemen proyek Agile, dengan pengalaman minimal satu tahun dalam pengembangan perangkat lunak Agile [M-5][M-6]. Analisis data dilakukan melalui Confirmatory Component Analysis (CCA) dan pengujian hipotesis untuk mengidentifikasi korelasi intra-variabel, serta penilaian keandalan data menggunakan Composite Reliability (CR) dan koefisien Cronbach [M-7]. Penelitian ini mengecualikan beberapa batasan proyek manajemen seperti jadwal dan biaya, dan lebih fokus pada batasan sumber daya, ruang lingkup proyek, dan risiko [M-8].

**Contoh real — sel Future Studies:**
Penelitian di masa depan harus mempertimbangkan pengujian hipotesis untuk parameter model yang berbeda antara kelompok studi, terutama saat membandingkan lebih dari dua kelompok, seperti Scrum dan Kanban [F-2]. Peneliti disarankan untuk menggunakan teknik confidence set mutakhir dalam analisis multi-kelompok untuk mengevaluasi kesesuaian berbagai pendekatan analisis multi-kelompok [F-2]. Penelitian lebih lanjut diperlukan untuk menyelidiki dampak inklusi kelompok pada fitur pengukuran dan struktural, karena asumsi ini sering kali tidak akurat [D-1][F-1].

**Contoh real — sel Method/Samples:**
Ukuran sampel populasi dalam penelitian ini adalah 102 responden, yang diambil dari 350 orang yang ditanyai, dengan menggunakan rumus sampling Cochran untuk menghitung ukuran sampel yang optimal [M-3]. Metode sampling yang digunakan adalah convenience sampling, yang melibatkan anggota tim yang bekerja dalam pengembangan perangkat lunak Agile dengan pengalaman minimal satu tahun [M-5]. Dari 102 responden, 63 menggunakan teknik Scrum, 38 menggunakan Kanban, 56 berada dalam peran manajerial, dan 32 merupakan bagian dari tim pengembangan perangkat lunak [M-5][M-6].

### Kolom custom (opsional — tambahkan setelah kolom default)

| ... | [Kolom custom 1] | [Kolom custom 2] |
|-----|------------------|------------------|
| ... | [isi] | [isi] |

## Master Data (untuk Export)

Simpan `papers.json` sesuai skema `references/table-builder.md` — mencakup metadata biblio
(authors list, journal, year, volume/issue/pages, doi, publisher, url, abstract, keywords) +
nilai tiap kolom. Semua format export diturunkan dari file ini.

## Ekspor Format

```bash
python3 scripts/export_formats.py papers.json --formats csv,xlsx,bib,xml,ris --out .
```

Menghasilkan `literature_table.csv`, `.xlsx`, `.bib`, `.xml`, `.ris`.

## Triase Pencarian

```
Dari [X] kandidat:
- Lolos relevansi ≥ 7/10 : [Y]
- Mode search : [a] | mode folder : [b] | hybrid : [c]
- DOI terverifikasi : [d] | UNVERIFIED : [e]
- Dibuang (relevansi < 7 / duplikat / tidak terbukti) : [f]
```

## Legenda

### Kode bagian paper (penanda sumber per kalimat)

| Kode | Bagian | Kode | Bagian |
|------|--------|------|--------|
| AB | Abstract | D | Discussion |
| I | Introduction | L | Limitations |
| M | Method | C | Conclusion |
| R | Results | F | Future Work |

Penanda `[M-2]` = klaim diambil dari bagian **Method**, **paragraf 2**. `[±n]` = nomor paragraf
perkiraan. Tiap kalimat dalam sel tabel harus ber-penanda (pada Mode Search hanya ada `[AB]`).

### Tanda lain

- `—` : data tidak tersedia / tidak ada di paper
- `(diringkas)` : field disimpulkan dari inferensi (bukan eksplisit)
- `(tidak eksplisit)` : tidak dinyatakan secara eksplisit di paper
- `UNVERIFIED` : keberadaan paper/DOI belum diverifikasi — cek manual