# Paper Review Skill

**Skill review & sintesis literatur untuk AI coding agents** (Claude Code, OpenCode, dan agen berbasis
Agent Skills lainnya). Memproduksi **tabel review paper** (synthesis matrix / literature review matrix)
dari dua sumber: (1) **pencarian online** berdasarkan topik + kata kunci + jumlah target, dan
(2) **folder lokal** berisi paper berformat PDF/LaTeX. Konten **bilingual** (Bahasa Indonesia / English).

Skill ini adalah subset terfokus dari [`bimajanuri/academic-writing-skill`](https://github.com/bimajanuri/academic-writing-skill)
— hanya bagian pencarian literatur + ekstraksi metadata + penyusunan tabel.

## Fitur Utama

- **Tiga mode input**: Search (pencarian online), Folder (baca PDF/LaTeX lokal), Hybrid (gabungan + dedup)
- **Tabel literature review (synthesis matrix)**: blok sitasi (Title & Authors, Journal, Year, DOI & Publisher)
  + blok ekstraksi (Purpose, Method, Key Findings, Limitations, Gaps, Theory Used, Novelty, Future Studies)
- **Sel komprehensif + provenance**: tiap kolom ekstraksi berisi 2–5 kalimat detail (bukan frasa pendek),
  dan setiap kalimat diberi **penanda sumber** `[KODE-n]` (bagian paper + nomor paragraf, mis. `[M-2]`) —
  sehingga tiap klaim dapat ditelusuri ke bagian paper (kode bagian + nomor paragraf)
- **Kolom custom**: user dapat menambah kolom apa saja (Relevance, Citations, Sampling Method, dll.)
- **Export 5 format** dari satu master data `papers.json`:
  CSV, Excel (XLSX), BibTeX (BIB), EndNote XML, RIS
- **Sumber pencarian gratis**: OpenAlex / Semantic Scholar / arXiv + web tools
- **Membaca PDF** via `scripts/extract_text.sh` (poppler) dan LaTeX dibaca langsung
- **Anti-hallucination**: tidak mengarang paper/DOI/isi kolom; tandai `UNVERIFIED`, `(diringkas)`, `—`
- **Triase & quality gate** dengan laporan statistik per pencarian

## Instalasi

### Claude Code

```bash
# Opsi 1 — symlink (kanonik, sekali update)
mkdir -p ~/.agents/skills
ln -s $(pwd) ~/.agents/skills/paper-review
ln -s ../../.agents/skills/paper-review ~/.claude/skills/paper-review

# Opsi 2 — salin langsung
cp -R . ~/.claude/skills/paper-review
```

### OpenCode

```bash
# Opsi 1 — symlink
ln -s ../../.agents/skills/paper-review ~/.config/opencode/skills/paper-review

# Opsi 2 — salin langsung
cp -R . ~/.config/opencode/skills/paper-review
```

> Rekomendasi: simpan repo ini sebagai kanonik di `~/.agents/skills/paper-review`, lalu **symlink** ke
> folder skills masing-masing klien. Edit cukup sekali di sumber.

## Penggunaan

Skill aktif otomatis saat user meminta, misalnya:

- "Cari 15 paper tentang X dan buatkan tabelnya"
- "Review semua paper di folder [path]"
- "Bikin tabel literatur dengan kolom tambahan Findings"
- "Kombinasi hasil search + folder saya"
- "Export tabel ke CSV/Excel/BibTeX/XML/RIS"
- "Export semua 5 format"

Aliran kerja: **Klarifikasi → Akuisisi paper → Ekstraksi per-field (papers.json) → Render tabel →
Export 5 format → Triase & quality gate.**

## Struktur Repo

```
paper-review/
├── SKILL.md                          # Pintu masuk & orchestrator
├── references/
│   ├── search-sources.md             # Pencarian online (OpenAlex/Semantic Scholar/arXiv)
│   ├── extracting-papers.md          # Baca folder PDF/LaTeX + ekstraksi per-field
│   └── table-builder.md              # Skema papers.json, render tabel, export 5 format
├── templates/
│   └── paper_review_table_template.md  # Template tabel review (synthesis matrix)
├── scripts/
│   ├── extract_text.sh               # Ekstraksi teks PDF via pdftotext
│   └── export_formats.py             # Export CSV/XLSX/BIB/XML/RIS dari papers.json
├── tests/
│   └── sample_papers.json            # Contoh data untuk verifikasi export
└── README.md
```

## Prasyarat Opsional

- **poppler-utils** (`pdftotext`) — untuk ekstraksi PDF: `brew install poppler` (macOS)
- **openpyxl** — untuk export Excel `.xlsx`: `pip3 install openpyxl`
- Tidak wajib bila hanya memakai metadata API / file LaTeX / Markdown

## Aturan Penting

1. **Output utama = tabel penuh per-paper** — setiap paper satu baris, semua kolom review terisi.
   Daftar kandidat/recap count hanyalah pelengkap, bukan pengganti tabel.
2. Tidak mengarang paper — setiap baris wajib punya DOI terverifikasi atau file lokal yang dibaca.
3. Tidak mengarang isi kolom — `—` untuk data tak tersedia, `(diringkas)` untuk inferensi.
4. Ambil klaim dari paper, bukan opini agent (kolom Novelty/Gaps).
5. Human-in-the-loop — agent mengusulkan, user memutuskan kolom, jumlah, dan definisi Gaps.
6. Reproducible — sertakan tanggal search, kata kunci, dan kombinasi yang dipakai.

## Attribution

Subset dari **bimajanuri/academic-writing-skill**, yang mengadaptasi metodologi dari
Master-cai/Research-Paper-Writing-Skills, SNL-UCSB/paper-writing-skill, dan WenyuChiou/ai-research-skills
(literature triage matrix). Struktur tabel (synthesis matrix) dan daftar format ekspor
(CSV/XLSX/BIB/XML/RIS) meniru fitur **Literature Review / Data Extraction** pada platform
reference-manager AI.

## Lisensi

Rilis di bawah **[MIT License](LICENSE)**.