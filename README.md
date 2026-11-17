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

**API resmi portal:** Open Data Surabaya punya CKAN API, tetapi `robots.txt`-nya melarang `/api/`. Karena itu dipakai API publik Open-Meteo, sesuai alternatif yang disebut soal.

## Cara menjalankan

Jalankan dari jaringan sendiri (laptop). Kuota harian Open-Meteo dihitung per IP, dan Wikimedia meminta User-Agent yang berisi kontak.

### Mac / Linux

```bash
git clone https://github.com/heyitsraditya/uts-dam-pariwisata-surabaya.git
```
```bash
cd uts-dam-pariwisata-surabaya
```
```bash
git checkout uts-dam-surabaya
```
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
cp .env.example .env
```
Buka `.env` dengan editor teks, lalu isi `CONTACT_EMAIL=` dengan email kontak Anda.
```bash
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 uts_dam.ipynb
```
```bash
python scripts/verify_submission.py
```

### Windows (PowerShell)

```powershell
git clone https://github.com/heyitsraditya/uts-dam-pariwisata-surabaya.git
```
```powershell
cd uts-dam-pariwisata-surabaya
```
```powershell
git checkout uts-dam-surabaya
```
```powershell
py -m venv .venv
```
```powershell
.venv\Scripts\Activate.ps1
```
Jika PowerShell menolak menjalankan skrip, jalankan sekali `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, lalu ulangi aktivasi.
```powershell
pip install -r requirements.txt
```
```powershell
Copy-Item .env.example .env
```
Buka `.env` dengan Notepad, lalu isi `CONTACT_EMAIL=` dengan email kontak Anda.
```powershell
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 uts_dam.ipynb
```
```powershell
python scripts\verify_submission.py
```

### Catatan saat eksekusi
- **Email kontak** dibaca dari environment variable `CONTACT_EMAIL`. Jika variabel itu tidak ada, notebook membacanya dari `.env`. Jika keduanya kosong, notebook berhenti dengan pesan *"CONTACT_EMAIL kosong. Buat .env dari .env.example dan isi CONTACT_EMAIL, atau set environment variable CONTACT_EMAIL."* Nilai email tidak pernah dicetak; output hanya menampilkan User-Agent dengan kontak disamarkan.
- **Jeda 10 detik:** `robots.txt` Open Data Surabaya menetapkan `Crawl-delay: 10`, jadi notebook menunggu minimal 10 detik antar-request ke portal itu. Seluruh eksekusi butuh sekitar 1–2 menit.
- **Menangani HTTP 429 (Too Many Requests):**
  - `etis_get()` otomatis mencoba ulang hingga 4 kali dengan jeda 2, 4, 8, dan 16 detik, atau sesuai header `Retry-After` jika ada.
  - Jika Open-Meteo membalas *"Daily API request limit exceeded"*, kuota harian untuk IP Anda habis. Notebook berhenti dengan pesan galat. Tunggu hingga hari berikutnya (atau pindah jaringan), lalu jalankan ulang perintah `nbconvert`. Berkas yang sudah terunduh tidak diunduh lagi.
  - Jika Wikipedia membalas 429, pastikan `CONTACT_EMAIL` terisi, tunggu beberapa menit, lalu jalankan ulang.
- **Tanggal akses** di `provenance.csv` diisi otomatis dari waktu unduh sebenarnya (WIB) dan disimpan di berkas pendamping `*.akses`. Notebook tidak memakai tanggal yang ditulis tangan.
- **Data mentah tidak pernah ditimpa:** berkas yang sudah ada di `data/raw/` dipakai apa adanya, dan MD5-nya dicocokkan ulang di akhir notebook. Untuk mengulang akuisisi dari awal, kosongkan `data/raw/` secara manual (sisakan `.gitkeep`).
- **Setelah lulus verifikasi**, commit hasilnya (`.env` otomatis diabaikan oleh `.gitignore`):
  ```bash
  git add uts_dam.ipynb data provenance.csv data_ethics_checklist.md
  ```

## Struktur folder

```
.
├── uts_dam.ipynb               # notebook tunggal (Setup, Soal 1–5, Ringkasan)
├── scripts/
│   └── verify_submission.py    # pemeriksaan LULUS/GAGAL setelah notebook dieksekusi
├── data/
│   ├── raw/                    # data mentah, immutable (+ berkas *.akses = tanggal akses)
│   │   ├── ckan_surabaya_wisman_wisnus_tempat_wisata.csv
│   │   ├── ckan_surabaya_dataset_page.html     # bukti metadata & lisensi
│   │   ├── ckan_surabaya_about.html            # bukti ketentuan/dasar hukum portal
│   │   ├── ckan_surabaya_robots.txt
│   │   ├── open_meteo_surabaya_harian_2025.json
│   │   ├── open_meteo_lisensi.html             # bukti lisensi CC BY 4.0
│   │   ├── open_meteo_ketentuan.html           # bukti ketentuan pemakaian API
│   │   ├── open_meteo_robots.txt
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
├── DEMO.md                     # skrip demo 5 menit + tanya-jawab
├── requirements.txt
├── .env.example                # contoh konfigurasi; .env asli tidak di-commit
└── .gitignore
```

Berkas di `data/raw/`, `data/processed/`, dan `provenance.csv` dihasilkan saat notebook dijalankan.

## Pemeriksaan `scripts/verify_submission.py`
1. Semua sel kode punya `execution_count` berurutan, tidak ada output error, dan setiap sel punya output.
2. Merge: 192 baris sebelum = sesudah, semua `both`, `duplicated().sum() == 0`, dan MD5 `gabungan.csv` cocok dengan metadata.
3. `provenance.csv`: URL, tanggal akses, lisensi, dan MD5 ada untuk setiap sumber; MD5 cocok dengan berkas di `data/raw/`; setiap berkas raw tercatat.
4. Berkas keluaran wajib tersedia dan sudah ter-track git.
5. `.env` tidak ter-track git, dan nilai `CONTACT_EMAIL` tidak muncul di berkas mana pun yang ter-track maupun di output notebook. Nilai itu tidak pernah dicetak.

## Etika akuisisi (ringkas)
- `robots.txt` diperiksa dengan `urllib.robotparser` sebelum akses (CKAN Surabaya, Wikipedia, Open-Meteo). CKAN Surabaya melarang `/api/`, jadi API CKAN tidak dipakai; `Crawl-delay: 10` ditegakkan.
- Setiap request memakai `timeout`, User-Agent jujur berisi kontak, jeda antar-request per host, dan retry dengan *exponential backoff* untuk 429/5xx.
- Tidak memakai sumber yang dilarang soal (Booking.com, Agoda, Traveloka, tiket.com, Airbnb, Tripadvisor, Google Maps, media sosial).
- Tidak ada API key. Soal meminta email kampus di User-Agent, tetapi mahasiswa tidak diberi email kampus, sehingga dipakai email pribadi yang hanya ada di `.env` lokal atau environment variable.

## Catatan kualitas data
- Kolom `tahun` berisi 2025 (12 bulan) dan 2026 (Jan–Okt). `TAHUN_DATA` diambil dari tahun yang lengkap 12 bulan, yaitu 2025.
- Satu nama destinasi punya spasi di ujung (`'ALUN ALUN SURABAYA BALAI PEMUDA '`). Spasi itu dibersihkan dengan `str.strip()` saat merge, dan perubahannya didokumentasikan.
- Nilai nol adalah data sah (tidak ada kunjungan tercatat), bukan data hilang.
- Angka **Juni dan Juli 2025 identik untuk ke-16 destinasi**. Ini dugaan kesalahan salin di sumber; temuan dilaporkan di notebook (Soal 1.5) dan `gabungan_metadata.json`, dan datanya tidak dikoreksi.
- Dataset kandidat lain yang dievaluasi saat seleksi tidak disimpan di repo dan tidak dipakai.

## Atribusi
- Data kunjungan wisatawan: Dinas Kebudayaan, Kepemudaan dan Olah Raga serta Pariwisata Kota Surabaya, melalui Open Data Surabaya (ckan.surabaya.go.id). Lisensi tidak dicantumkan; dipakai untuk keperluan akademik.
- Data cuaca: [Open-Meteo.com](https://open-meteo.com/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Tabel kecamatan: kontributor Wikipedia, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
