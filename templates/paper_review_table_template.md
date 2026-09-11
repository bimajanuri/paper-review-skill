# Template Tabel Review Paper (Paper Review Table)

Salin struktur ini untuk output tabel. Default **8 kolom** + ruang untuk kolom custom.
Isi `—` bila data tidak tersedia di paper/sumber.

## Metadata Pencarian

- **Mode**: [Search / Folder / Hybrid]
- **Topik**: [topik penelitian]
- **Kata kunci**: [keyword + kombinasi yang dipakai]
- **Jumlah target**: [N] | **Jumlah baris**: [M]
- **Rentang tahun**: [YYYY–YYYY] | **Tanggal**: [YYYY-MM-DD]
- **Sumber**: [OpenAlex / Semantic Scholar / arXiv / Folder: <path> / kombinasi]

## Tabel Review

| No | Authors/Title | Purpose | Gaps | Method (Variables/Samples) | Theory Used | Novelty/Contribution | Future Studies | Source (DOI & Publisher) |
|----|---------------|---------|------|---------------------------|-------------|----------------------|----------------|--------------------------|
| 1  | [Penulis (Tahun)] — "[Judul]" | [Tujuan 1 kalimat] | [gap yang di-address / limitations] | Desain; IV; DV; n=; sampel; instrumen; analisis | [Teori / Tidak disebut eksplisit] | [klaim kontribusi] | [saran lanjutan / —] | DOI: 10.xxxx/... \| [Jurnal/Penerbit] \| [Tahun] |
| 2  | | | | | | | | |
| ... | | | | | | | | |

### Kolom custom (opsional — tambahkan setelah kolom default)

| ... | [Kolom custom 1] | [Kolom custom 2] |
|-----|------------------|------------------|
| ... | [isi] | [isi] |

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