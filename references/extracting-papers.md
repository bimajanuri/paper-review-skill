# Extracting Papers — Membaca Folder PDF/LaTeX & Ekstraksi Per-Field

Panduan untuk **Mode B (Folder)** dan bagian ekstraksi isi tabel.

## 1. Skema Klasifikasi File

| Ekstensi | Penanganan |
|----------|------------|
| `*.tex` | Baca langsung sebagai teks (structured source, mudah diekstrak: title/abstract per section) |
| `*.pdf` | Ekstrak teks dulu (lihat di bawah) |
| `*.md / *.docx` | Bisa juga diproses bila ada (bagi ekstraksi jadi dari text) |
| lainnya | Abaikan, beri tahu user |

Menemukan file: gunakan glob (`**/*.pdf`, `**/*.tex`) mulai dari folder yang ditunjuk user, termasuk subfolder.

## 2. Ekstraksi Teks PDF

### Cara cepat (tanpa script tambahan)
- **poppler-utils**: `pdftotext <file.pdf> -` → teks langsung ke stdout.
- **pypdf / pdfplumber** bila tersedia: `python3 -c "import pypdf; ..."`.

### Via script skill
```
scripts/extract_text.sh <folder-atau-file.pdf>
```
Membuat file `.txt` sejajar untuk tiap PDF di folder (rekursif). Lihat header script untuk dependensi.

### PDF hasil scan / OCR
Bila output teks kosong/gambar, bilang ke user "PDF tampaknya hasil scan".
Cek ada tidaknya `pdftotext -layout` perbaikan; OCR (tesseract) opsional bila tersedia dan user mengizinkan.
Untuk paper yang tak terbaca → isi dari metadata API (DOI di halaman PDF) saja, field lain `—`.

## 3. Lokasi Konten per Kolom (di dalam paper)

Baca bagian paper dalam urutan ini:

| Kolom | Tempat di paper | Petunjuk |
|-------|-----------------|----------|
| **Title & Authors / Journal / Year** | Halaman judul, header LaTeX `\title`, `\author`, metadata | Format ringkas: `Penulis1, Penulis2, & Penulis3`. > 6 penulis → `Penulis1 et al.` |
| **Purpose** | Abstract & Introduction | Cari frasa: "this study aims", "we examine", "penelitian ini bertujuan". 1 kalimat; tidak eksplisit → ringkas + tandai `(diringkas)` |
| **Method (Variables/Samples)** | Method section | Desain; IV/DV; `n=...`; populasi & sampling; instrumen; analisis (regresi, SEM/PLS, ANOVA, dll.) |
| **Key Findings** | Abstract & Results | Hasil utama + angka kunci (efek, koefisien, p-value, n) |
| **Limitations** | Discussion / Limitations (akhir paper) | Frasa "limitation", "cannot", "our study was limited". Tidak ada → `—` |
| **Gaps** | Introduction (gap yang di-address) ATAU pembahasan (sesuai kesepakatan Step 0) | Gap yang di-address: "little is known", "few studies", "no study has". Untuk makna gap riset baru: rekomendasi implisit penulis | 
| **Theory Used** | Introduction / Literature Review | Nama teori/kerangka (mis. Theory of Planned Behavior). Tidak eksplisit → `Tidak disebut eksplisit` |
| **Novelty/Contribution** | Introduction & Conclusion | Ambil klaim paper: "we contribute", "first to", "novel". JANGAN opini sendiri |
| **Future Studies** | Future Work / Conclusion | Salin/ringkas saran lanjutan. Tidak ada → `—` |
| **DOI & Publisher** | Halaman judul/header/footer, metadata logger | `DOI: 10.xxxx/... \| Penerbit` |

Untuk `.tex`, ekstraksi lebih mudah: `\title{}`, `\author{}`, `\begin{abstract}...`, section `\section{Method}`.

## 3a. Mengisi Sel Komprehensif + Penanda Sumber (Data Extraction)

Sel tabel berisi **2–5 kalimat lengkap** (bukan frasa pendek) yang merangkum detail paper, dan tiap
kalimat/klaim diakhiri **penanda sumber `[KODE-n]`**: kode bagian + nomor paragraf di bagian tsb.

**Kode bagian:** `AB` Abstract · `I` Introduction · `M` Method · `R` Results · `D` Discussion ·
`L` Limitations · `C` Conclusion · `F` Future Work

Contoh kolom Future Studies (3 kalimat, masing-masing ber-penanda):
```
"Penelitian lanjutan perlu menguji hipotesis parameter model yang berbeda antar kelompok,
terutama membandingkan > 2 kelompok, mis. Scrum vs Kanban [F-2]. Disarankan memakai teknik
confidence set mutakhir dalam analisis multi-kelompok untuk mengevaluasi kesesuaian pendekatan
[F-2]. Studi lebih lanjut diperlukan untuk menyelidiki dampak inklusi kelompok pada fitur
pengukuran dan struktural karena asumsinya sering tidak akurat [D-1][F-1]."
```

Contoh kolom Method (detail: desain, sampling, analisis, pengecualian):
```
"Penelitian memakai analisis komparatif statistik untuk membandingkan efektivitas metode
Kanban dan Scrum pada proyek Agile berbiaya dan berjadwal tetap [M-2]. Pengumpulan data
menggunakan convenience sampling dari para ahli manajemen proyek Agile berpengalaman ≥ 1 tahun
[M-5][M-6]. Analisis data via Confirmatory Component Analysis (CCA), uji hipotesis korelasi
intra-variabel, dan reliabilitas dengan Composite Reliability (CR) & Cronbach [M-7]. Studi
mengecualikan batasan jadwal dan biaya, fokus pada sumber daya, ruang lingkup, dan risiko [M-8]."
```

Aturan:
1. Penanda diletakkan **persis setelah kalimat** sumbernya; gabungan → `[D-1][F-1]`.
2. Paragraf dinomori dari awal bagian; Keliru ragu → tandai `[±n]` (perkiraan).
3. **Mode Folder** → penanda bagian+paragraf nyata. **Mode Search** (hanya abstract) → sel lebih
   ringkas, penanda `[AB]`. Jangan mengarang detail yang tidak ada di sumber.
4. Kolom yang di paper tidak punya konten → `—` (jangan menulis dari opini).
5. Untuk `.tex`, nomor paragraf mengikuti struktur `.tex` (mis. paragraf ke-2 di `\section{Method}`).

## 3b. Metadata Biblio untuk Export Sitasi

Export `.bib`/`.ris`/`.xml` butuh metadata lengkap. Kalau tersedia di metadata API (OpenAlex
`biblio`/`primary_location`, Semantic Scholar `externalIds`/`venue`) atau di file, kumpulkan:
`title`, `authors` (**list**, format `Surname, Given`, > 6 penulis tetap simpan semua — cuti di tabel saja,
tidak di file sitasi), `year`, `journal`, `volume`, `issue`, `pages`, `doi`, `publisher`, `url`,
`abstract`, `keywords`.

Field yang tidak tersedia → **string kosong `""`** (bukan `—`) di JSON, agar tidak ikut ter-export.
`openalex` juga menyediakan keywords/topics bila perlu.

## 4. Fallback Data

- Bila file lokal tak lengkap (mis. DOI statusnya paywalled, abstract kosong):
  coba dapatkan metadata dari **OpenAlex/Semantic Scholar** menggunakan judul dari file → isi yang kosong.
- Abstract tidak tersedia di mana pun → kolom Purpose/Method ringkas diisi `—`.

## 5. Anti-Hallucination (Wajib)

1. Jangan mengarang isi kolom — file yang tidak terbaca → `—`, bukan menebak.
2. Klaim kebaruan/teori diambil dari teks paper; bila tidak ada → tandai sesuai.
3. DOI di file yang belum diverifikasi → `UNVERIFIED`.
4. Dua file yang sama (duplikat DOI/judul) → jaga satu baris.

## 6. Output Per Ekstraksi

Untuk jumlah paper besar (> 10), simpan draft ekstraksi per paper dulu:
```
extraction_draft.md  — per paper: sumber file + hasil baca per kolom
```
Kemudian render ke tabel lewat `table-builder.md`.