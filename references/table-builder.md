# Table Builder — Render Tabel Review

Panduan merakit output tabel (Markdown/CSV) dari hasil ekstraksi, termasuk kolom custom.

## 1. Definisikan Kolom Dulu

Di Step 0 user menyepakati kolom. Contoh resolusi kolom:

| Mode | Header |
|------|--------|
| **Default (8 kolom)** | `No | Authors/Title | Purpose | Gaps | Method (Variables/Samples) | Theory Used | Novelty/Contribution | Future Studies | Source (DOI & Publisher)` |
| **Default + Relevance** | header di atas + `Relevance (0–10)` |
| **Kolom custom lain** | di-append atau mengikuti urutan yang user mau (mis. `Findings`, `Quartile`, `Screenshot`, `Referensi Lain`) |

**Kolom custom** diisi dengan:
- isi paper (mis. `Findings` = angka/hasil utama dari Results), atau
- hasil pertanyaan tambahan yang diminta user (mis. "tandai mana yang teoritis vs empiris").

Hapus kolom default hanya bila user eksplisit memintanya. Jaga header singkat & konsisten untuk semua baris.

## 2. Isi Sel

- Satu **baris per paper**. Nilai sel ringkas (target ≤ ~40 kata; panjangkan hanya bila perlu, mis. Method).
- Data tidak tersedia → `—` (jangan biarkan sel kosong tanpa makna).
- Inferensi → tambahkan `(diringkas)`; tidak eksplisit → `(tidak eksplisit)`.
- DOI yang belum terverifikasi → `UNVERIFIED`.
- Untuk sel berisi list, gunakan titik koma (`;`) sebagai pemisah, bukan baris baru (menjaga CSS:
  agar tidak merusak format tabel di markdown).

## 3. Render Markdown

```markdown
| No | Authors/Title | Purpose | Gaps | ... |
|----|---------------|---------|------|-----|
| 1  | ... | ... | ... | ... |
```

Di atas tabel, sertakan **Metadata Pencarian**:

```markdown
- Mode: Search / Folder / Hybrid
- Topik: ...
- Kata kunci: ... (tambahkan kombinasi yang dipakai)
- Jumlah target: N | Jumlah baris: M
- Rentang tahun: YYYY–YYYY | Tanggal: YYYY-MM-DD
- Sumber: OpenAlex / Semantic Scholar / Folder: <path> / kombinasi
```

Di bawah tabel, sertakan **Legenda**:

```markdown
## Legenda
- `—` : data tidak tersedia
- `(diringkas)` : disimpulkan dari inferensi
- `(tidak eksplisit)` : tidak dinyatakan di paper
- `UNVERIFIED` : keberadaan/DOI belum diverifikasi — cek manual
```

## 4. Render CSV (Opsional)

- Header = nama kolom, satu baris per paper.
- Pisahkan koma; nilai yang mengandung koma/kutip/baris-baru dibungkus `"..."` (gandakan `"` di dalamnya).
- Semi-colon atau tab dapat dipakai bila user menggunakan Excel lokal berbahasa Indonesia (`;` diterima) —
  tanya atau beri tahu format yang dipakai.

## 5. Validasi Tabel

Sebelum menyerahkan:
1. Jumlah baris == jumlah paper lolos (sesuai triase).
2. Semua header kolom yang disepakati hadir; tidak ada kolom tanpa isi untuk semua baris (kecuali memang `—`).
3. Tidak ada sel kosong (spasi kosong) — selalu isi `—`.
4. DOI menjorok konsisten (`DOI: 10.xxxx/...`) untuk kolom Source.
5. Jika tabel MD akan dikonversi (Excel/Google Sheets), sarankan CSV.

## 6. Output

```
literature_table.md   — tabel final markdown
literature_table.csv  — opsional, bila diminta
```

Tabel ini siap dipakai untuk Gap Analysis lanjutan (lihat academic-writing-skill Tahap 1.4) atau
sintesis literatur.