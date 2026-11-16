# UTS Data Acquisition & Management — Pariwisata Surabaya

**Topik:** Kunjungan wisatawan per destinasi wisata dan cuaca bulanan Kota Surabaya, 2025.
Mata kuliah Data Acquisition & Management, Informatika Kelas E, INSTIKI. Dosen: Dr. I Gede Totok Suryawan.

Seluruh akuisisi, pembersihan, dan penggabungan data ada di **satu notebook**: `uts_dam.ipynb`.

## Ringkasan sumber

| Sumber | Jenis | Isi | Lisensi |
|---|---|---|---|
| (a) [Open Data Surabaya](https://ckan.surabaya.go.id/dataset/banyaknya-kunjungan-wisatawan-nusantara-dan-wisatawan-mancanegara-menurut-tempat-wisata-tahun-2025): *Banyaknya Kunjungan Wisatawan Nusantara dan Wisatawan Mancanegara menurut Tempat Wisata* (Disbudporapar Kota Surabaya) | Berkas CSV (pemisah `;`) | 352 baris × 9 kolom, 16 destinasi; Jan 2025 s.d. Okt 2026. Analisis memakai 2025 (192 baris, 12 bulan). | Tidak dicantumkan di metadata CKAN ("No License Provided") |
| (b) [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) | API JSON (tanpa key) | Cuaca harian 1 titik Kota Surabaya (lat -7.2575, lon 112.7521), 1 Jan–31 Des 2025 → 365 baris harian → 12 baris bulanan | CC BY 4.0 |
| (c) [Wikipedia ID: Daftar kecamatan dan kelurahan di Kota Surabaya](https://id.wikipedia.org/wiki/Daftar_kecamatan_dan_kelurahan_di_Kota_Surabaya) | Scraping HTML | 31 kecamatan (kode Kemendagri, kodepos, jumlah kelurahan); hanya untuk Soal 4 | CC BY-SA 4.0 |

**Merge (Soal 5):** (a) × (b) pada kunci `bulan`, `validate="many_to_one"`, `indicator=True` → `data/processed/gabungan.csv`.
Tabel (c) tidak ikut di-merge karena data kunjungan tidak punya kolom kecamatan.

## Cara menjalankan

Disarankan dijalankan dari laptop/jaringan sendiri. Kuota harian Open-Meteo dihitung per IP, dan Wikimedia mewajibkan User-Agent yang berisi kontak.

1. Siapkan lingkungan Python 3.10+:
   ```bash
   python -m venv .venv
   ```
   ```bash
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```
   ```bash
   pip install -r requirements.txt
   ```
2. Buat `.env` dari contoh dan isi email kontak (dipakai di User-Agent):
   ```bash
   cp .env.example .env
   ```
   Lalu ubah baris `CONTACT_EMAIL=` di `.env`. Jika `.env` belum ada atau masih berisi contoh, notebook berhenti dengan pesan *"Buat .env dari .env.example dan isi CONTACT_EMAIL"*.
3. Jalankan seluruh notebook dari nol dan simpan outputnya:
   ```bash
   jupyter nbconvert --to notebook --execute --inplace uts_dam.ipynb
   ```
   Lama eksekusi sekitar 1 menit, karena notebook menunggu `Crawl-delay: 10` detik antar-request ke portal CKAN.

**Perilaku data mentah:** notebook hanya mengunduh berkas yang belum ada di `data/raw/`. Berkas yang sudah ada tidak pernah ditimpa; MD5-nya dihitung ulang dan dibandingkan dengan `provenance.csv` di akhir notebook. Tanggal akses setiap berkas mentah disimpan di berkas pendamping `*.akses`. Untuk mengulang akuisisi dari awal, kosongkan `data/raw/` secara manual (kecuali `.gitkeep`).

## Struktur folder

```
.
├── uts_dam.ipynb               # notebook tunggal (Setup, Soal 1–5, Ringkasan)
├── data/
│   ├── raw/                    # data mentah, immutable (+ berkas *.akses = tanggal akses)
│   │   ├── ckan_surabaya_wisman_wisnus_tempat_wisata.csv
│   │   ├── ckan_surabaya_dataset_page.html     # bukti metadata & lisensi
│   │   ├── ckan_surabaya_about.html            # bukti ketentuan/dasar hukum portal
│   │   ├── ckan_surabaya_robots.txt
│   │   ├── open_meteo_surabaya_harian_2025.json
│   │   ├── wikipedia_kecamatan_surabaya.html
│   │   └── wikipedia_id_robots.txt
│   └── processed/
│       ├── cuaca_harian_surabaya.csv
│       ├── cuaca_bulanan_surabaya.csv
│       ├── kecamatan_surabaya.csv
│       ├── gabungan.csv
│       └── gabungan_metadata.json
├── provenance.csv              # URL, tanggal akses, lisensi, MD5, metode tiap sumber
├── data_ethics_checklist.md    # 9 butir (dibuat ulang oleh notebook)
├── DEMO.md                     # skrip demo 3–5 menit + tanya-jawab
├── requirements.txt
├── .env.example                # contoh konfigurasi; .env asli tidak di-commit
└── .gitignore
```

Berkas di `data/raw/`, `data/processed/`, dan `provenance.csv` dihasilkan saat notebook dijalankan.

## Etika akuisisi (ringkas)
- `robots.txt` diperiksa dengan `urllib.robotparser` sebelum akses. CKAN Surabaya melarang `/api/`, jadi API CKAN tidak dipakai; `Crawl-delay: 10` ditegakkan.
- Setiap request memakai `timeout`, User-Agent jujur berisi kontak, jeda antar-request per host, dan retry dengan *exponential backoff* untuk 429/5xx (menghormati `Retry-After`).
- Tidak memakai sumber yang dilarang soal (Booking.com, Agoda, Traveloka, tiket.com, Airbnb, Tripadvisor, Google Maps, media sosial).
- Tidak ada API key. Email kontak hanya ada di `.env` lokal.

## Catatan kualitas data
- Kolom `tahun` berisi 2025 (12 bulan) dan 2026 (Jan–Okt). `TAHUN_DATA` diambil dari tahun yang lengkap 12 bulan, yaitu 2025.
- Satu nama destinasi punya spasi di ujung (`'ALUN ALUN SURABAYA BALAI PEMUDA '`). Spasi itu dibersihkan dengan `str.strip()` saat merge, dan perubahannya didokumentasikan.
- Angka **Juni dan Juli 2025 identik untuk ke-16 destinasi**. Ini dugaan kesalahan salin di sumber; temuan dilaporkan di notebook (Soal 1.5) dan `gabungan_metadata.json`, dan datanya tidak dikoreksi.
- Dataset kandidat lain yang dievaluasi saat seleksi (*Jumlah Hotel per Kecamatan* dan *Jumlah kunjungan wisatawan di objek wisata*) hanya diunduh sementara untuk pengecekan jumlah baris. Keduanya tidak disimpan di repo dan tidak dipakai.

## Atribusi
- Data kunjungan wisatawan: Dinas Kebudayaan, Kepemudaan dan Olah Raga serta Pariwisata Kota Surabaya, melalui Open Data Surabaya (ckan.surabaya.go.id). Lisensi tidak dicantumkan; dipakai untuk keperluan akademik.
- Data cuaca: [Open-Meteo.com](https://open-meteo.com/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data reanalisis ERA5 dari Copernicus/ECMWF.
- Tabel kecamatan: kontributor Wikipedia, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
