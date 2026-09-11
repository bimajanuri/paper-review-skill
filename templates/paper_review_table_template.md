# Template Tabel Review Paper (SciSpace-Style)

Salin struktur ini untuk output tabel. **Blok sitasi + blok ekstraksi** (ala SciSpace Literature Review)
+ ruang kolom custom. Isi `—` bila data tidak tersedia di paper/sumber.

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
| 1  | [Penulis (Tahun)] — "[Judul]" | [Jurnal] | [Tahun] | [Tujuan 1 kalimat] | Desain; IV; DV; n=; sampel; instrumen; analisis | [hasil + angka kunci] | [keterbatasan / —] | [gap yang di-address] | [Teori / Tidak disebut eksplisit] | [klaim kontribusi] | [saran lanjutan / —] | DOI: 10.xxxx/... \| [Penerbit] |
| 2  | | | | | | | | | | | | |
| ... | | | | | | | | | | | | |

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

- `—` : data tidak tersedia / tidak ada di paper
- `(diringkas)` : field disimpulkan dari inferensi (bukan eksplisit)
- `(tidak eksplisit)` : tidak dinyatakan secara eksplisit di paper
- `UNVERIFIED` : keberadaan paper/DOI belum diverifikasi — cek manual