# UTS Data Acquisition & Management — Pariwisata Surabaya

**Topik:** Kunjungan wisatawan per destinasi wisata dan cuaca bulanan Kota Surabaya, 2025.
Mata kuliah Data Acquisition & Management, Informatika Kelas E, INSTIKI. Dosen: Dr. I Gede Totok Suryawan, S.Kom., M.T.

| | |
|---|---|
| Nama | I Gede Raditya Ananda Putra|
| NIM | 2501010024 |

Seluruh akuisisi, pembersihan, dan penggabungan data ada di **satu notebook**: `uts_dam.ipynb`.

## Ringkasan sumber

| Sumber | Jenis | Isi | Lisensi |
|---|---|---|---|
| (a) **data.go.id**: [*Banyaknya Kunjungan Wisatawan Nusantara dan Wisatawan Mancanegara menurut Tempat Wisata*](https://data.go.id/dataset/dataset/banyaknya-kunjungan-wisatawan-nusantara-dan-wisatawan-mancanegara-menurut-tempat-wisata-ta-2025), organisasi Kota Surabaya, Dataset ID `5c1cb1a5-8b39-42df-a8c3-48fff07fec6e` | Berkas CSV `banyaknya-wisman-wisnus-2026.csv` (pemisah `;`) | 352 baris × 9 kolom, 16 destinasi; Januari 2025 s.d. Oktober 2026. Analisis memakai 2025 (192 baris, 12 bulan). | Lisensi tidak dicantumkan pada tabel metadata halaman dataset data.go.id. Status akses di portal: Terbuka. |
| (b) [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) | API JSON (tanpa key) | Cuaca harian 1 titik Kota Surabaya (lat -7.2575, lon 112.7521), 1 Januari–31 Desember 2025 → 365 baris harian → 12 baris bulanan | CC BY 4.0 (diverifikasi otomatis dari halaman lisensi saat eksekusi) |
| (c) [Wikipedia ID: Daftar kecamatan dan kelurahan di Kota Surabaya](https://id.wikipedia.org/wiki/Daftar_kecamatan_dan_kelurahan_di_Kota_Surabaya) | Scraping HTML | 31 kecamatan (kode Kemendagri, kodepos, jumlah kelurahan); hanya untuk Soal 4 | CC BY-SA 4.0 |

### Peran pihak pada sumber (a)

| Peran | Pihak |
|---|---|
| Katalog (tempat dataset ditemukan dan diunduh; termasuk sumber yang diizinkan soal) | data.go.id |
| Host berkas (tujuan tombol *Download*) | ckan.surabaya.go.id — tautan: `https://ckan.surabaya.go.id/dataset/5c1cb1a5-8b39-42df-a8c3-48fff07fec6e/resource/3a969972-e959-462d-b37b-cbdd14830f0b/download/banyaknya-wisman-wisnus-2026.csv` |
| Penerbit asli | Pemerintah Kota Surabaya |

Berkas diunduh **manual lewat peramban oleh mahasiswa** dengan tombol *Download* di halaman data.go.id pada **17 November 2026**. MD5: `2658a38dff0ec62756fbd1147fd6914a`. Bukti tangkapan layar metadata: `docs/bukti_metadata_data_go_id_2026-11-17.png`. Notebook juga mengunduh ulang tautan yang sama dengan skrip (Soal 1.9), lalu membandingkan MD5-nya.

### Ketidakcocokan metadata katalog dengan isi berkas
1. Label resource menyebut cakupan "per Januari 2025 - Agustus 2026", padahal berkas memuat data hingga **Oktober 2026**.
2. Metadata terakhir dimodifikasi **25-09-2026**, padahal berkas memuat data Oktober 2026.
3. Slug URL halaman berakhiran **`-ta-2025`**, padahal berkas memuat 2025 dan 2026.

**Penjelasannya:** data.go.id berperan sebagai katalog metadata, sedangkan tombol *Download* mengarah ke berkas di ckan.surabaya.go.id dengan Dataset ID yang sama. Metadata katalog tidak ikut diperbarui, sementara berkas di CKAN diperbarui hingga Oktober 2026. Karena isi berkas bisa berubah tanpa perubahan metadata katalog, **MD5 dan tanggal unduh adalah bukti utama**.

Halaman dataset juga menampilkan banner *"INFORMASI: Data berikut ini masih dalam proses pemenuhan Prinsip SDI."*, dan tabel metadatanya kosong untuk semua kolom.

**Merge (Soal 5):** (a) × (b) pada kunci `bulan`, `validate="many_to_one"`, `indicator=True` → `data/processed/gabungan.csv`.
Tabel (c) tidak ikut di-merge karena data kunjungan tidak punya kolom kecamatan.

**API resmi portal:** API yang melayani berkas ini adalah CKAN API di host berkas, dan `robots.txt` host itu melarang `/api/`. Karena itu dipakai API publik Open-Meteo, sesuai alternatif yang disebut soal.

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
Buka `.env` dengan editor teks, lalu isi `CONTACT_EMAIL=` dengan email kontak Anda. Setelah itu salin berkas `banyaknya-wisman-wisnus-2026.csv` hasil unduhan data.go.id ke `data/raw/` tanpa mengubah nama atau isinya.
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
Buka `.env` dengan Notepad, lalu isi `CONTACT_EMAIL=` dengan email kontak Anda. Setelah itu salin berkas `banyaknya-wisman-wisnus-2026.csv` hasil unduhan data.go.id ke `data\raw\` tanpa mengubah nama atau isinya.
```powershell
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 uts_dam.ipynb
```
```powershell
python scripts\verify_submission.py
```

### Catatan saat eksekusi
- **Email kontak** dibaca dari environment variable `CONTACT_EMAIL`. Jika variabel itu tidak ada, notebook membacanya dari `.env`. Jika keduanya kosong, notebook berhenti dengan pesan *"CONTACT_EMAIL kosong. Buat .env dari .env.example dan isi CONTACT_EMAIL, atau set environment variable CONTACT_EMAIL."* Nilai email tidak pernah dicetak; output hanya menampilkan User-Agent dengan kontak disamarkan.
- **Berkas utama wajib ada:** jika `data/raw/banyaknya-wisman-wisnus-2026.csv` belum ada, notebook berhenti dengan pesan yang menjelaskan cara menaruhnya.
- **Jeda 10 detik:** `robots.txt` ckan.surabaya.go.id menetapkan `Crawl-delay: 10`, jadi notebook menunggu minimal 10 detik antar-request ke host itu. Seluruh eksekusi butuh sekitar 1–2 menit.
- **Verifikasi tautan unduhan (Soal 1.9) tidak pernah menggagalkan notebook.** Jika host CKAN tidak terjangkau, diblokir, atau ditolak `robots.txt`, statusnya dicatat dan notebook lanjut. Jika MD5 berbeda dari unduhan manual (berkas di CKAN diperbarui lagi), perbedaannya ditampilkan.
- **Menangani HTTP 429 (Too Many Requests):**
  - `etis_get()` otomatis mencoba ulang hingga 4 kali dengan jeda 2, 4, 8, dan 16 detik, atau sesuai header `Retry-After` jika ada.
  - Jika Open-Meteo membalas *"Daily API request limit exceeded"*, kuota harian untuk IP Anda habis. Notebook berhenti dengan pesan galat. Tunggu hingga hari berikutnya (atau pindah jaringan), lalu jalankan ulang perintah `nbconvert`. Berkas yang sudah terunduh tidak diunduh lagi.
  - Jika Wikipedia membalas 429, pastikan `CONTACT_EMAIL` terisi, tunggu beberapa menit, lalu jalankan ulang.
- **Tanggal akses:**
  - Sumber utama (data.go.id): **17 November 2026**, tanggal unduhan manual (statis).
  - Sumber lain (verifikasi CKAN, Open-Meteo, Wikipedia, robots.txt): diisi otomatis dari waktu unduh sebenarnya (WIB) dan disimpan di berkas pendamping `*.akses`.
- **Data mentah tidak pernah ditimpa:** berkas yang sudah ada di `data/raw/` dipakai apa adanya, dan MD5-nya dicocokkan ulang di akhir notebook.
- **Bukti Open-Meteo diverifikasi otomatis:** saat eksekusi, kode mencari frasa "CC BY 4.0", "non-commercial", dan "10,000" di halaman lisensi dan ketentuan yang diunduh, lalu menampilkan kutipannya. Frasa yang tidak ditemukan ditandai `TIDAK DITEMUKAN`, dan `verify_submission.py` memberi PERINGATAN agar halamannya Anda periksa manual (misalnya karena penulisan angka di halaman berbeda).
- **Alasan API (Soal 3.1):** isi bagian data.go.id yang masih berupa placeholder (tanda kurung siku bertuliskan ISI SEBELUM KUMPUL) dengan hasil pemeriksaan Anda: apakah data.go.id menyediakan API publik terdokumentasi untuk mengambil isi dataset ini.
- **Setelah lulus verifikasi**, tambahkan tangkapan layar metadata lalu commit hasilnya (`.env` otomatis diabaikan oleh `.gitignore`):
  ```bash
  git add uts_dam.ipynb data docs provenance.csv data_ethics_checklist.md README.md
  ```

## Struktur folder

```
.
├── uts_dam.ipynb               # notebook tunggal (Setup, Soal 1–5, Ringkasan)
├── scripts/
│   └── verify_submission.py    # pemeriksaan LULUS/GAGAL/PERINGATAN setelah notebook dieksekusi
├── docs/
│   └── bukti_metadata_data_go_id_2026-11-17.png   # tangkapan layar metadata (ditambahkan mahasiswa)
├── data/
│   ├── raw/                    # data mentah, immutable (+ berkas *.akses = tanggal akses unduhan skrip)
│   │   ├── banyaknya-wisman-wisnus-2026.csv      # sumber utama: unduhan manual data.go.id
│   │   ├── ckan_check/banyaknya-wisman-wisnus-2026.csv   # unduhan skrip dari tautan yang sama (verifikasi)
│   │   ├── ckan_surabaya_robots.txt
│   │   ├── open_meteo_surabaya_harian_2025.json
│   │   ├── open_meteo_lisensi.html               # bukti lisensi
│   │   ├── open_meteo_ketentuan.html             # bukti ketentuan pemakaian API
│   │   ├── open_meteo_robots.txt
│   │   ├── wikipedia_kecamatan_surabaya.html
│   │   └── wikipedia_id_robots.txt
│   └── processed/
│       ├── kunjungan_bersih_bertanda.csv          # salinan dengan nama di-strip + kolom diduga_salinan
│       ├── cuaca_harian_surabaya.csv
│       ├── cuaca_bulanan_surabaya.csv
│       ├── kecamatan_surabaya.csv
│       ├── gabungan.csv
│       └── gabungan_metadata.json
├── provenance.csv              # URL, tanggal akses, lisensi, MD5, cara perolehan, bukti tiap sumber
├── data_ethics_checklist.md    # 9 butir (dibuat ulang oleh notebook)
├── DEMO.md                     # skrip demo 5 menit + tanya-jawab
├── requirements.txt
├── .env.example                # contoh konfigurasi; .env asli tidak di-commit
└── .gitignore
```

`data/raw/banyaknya-wisman-wisnus-2026.csv` dan `docs/bukti_metadata_data_go_id_2026-11-17.png` ditambahkan oleh mahasiswa. Berkas lain di `data/`, serta `provenance.csv`, dihasilkan saat notebook dijalankan.

## Pemeriksaan `scripts/verify_submission.py`
1. Semua sel kode punya `execution_count` berurutan, tidak ada output error, dan setiap sel punya output.
2. Merge: 192 baris sebelum = sesudah, semua `both`, `duplicated().sum() == 0`, dan MD5 `gabungan.csv` cocok dengan metadata.
3. `provenance.csv`:
   - URL, tanggal akses, lisensi, dan MD5 ada untuk setiap sumber, dan MD5 cocok dengan berkas di `data/raw/`.
   - Setiap berkas raw, termasuk yang di subfolder, tercatat.
   - Baris sumber utama memuat domain data.go.id dan tanggal 17 November 2026.
4. Berkas keluaran wajib tersedia dan sudah ter-track git. **GAGAL** jika masih ada placeholder (tanda kurung siku bertuliskan ISI SEBELUM KUMPUL); **PERINGATAN** jika tangkapan layar bukti belum ada atau ada frasa bukti Open-Meteo yang tidak ditemukan.
5. `.env` tidak ter-track git, dan nilai `CONTACT_EMAIL` tidak muncul di berkas mana pun yang ter-track maupun di output notebook. Nilai itu tidak pernah dicetak.

## Etika akuisisi (ringkas)
- `robots.txt` diperiksa dengan `urllib.robotparser` sebelum akses (ckan.surabaya.go.id, Open-Meteo, Wikipedia). Path `/api/` CKAN dilarang dan tidak dipakai; `Crawl-delay: 10` ditegakkan.
- Setiap request memakai `timeout`, User-Agent jujur berisi kontak, jeda antar-request per host, dan retry dengan *exponential backoff* untuk 429/5xx.
- Tidak memakai sumber yang dilarang soal (Booking.com, Agoda, Traveloka, tiket.com, Airbnb, Tripadvisor, Google Maps, media sosial).
- Tidak ada API key. Soal meminta email kampus di User-Agent, tetapi mahasiswa tidak diberi email kampus, sehingga dipakai email pribadi yang hanya ada di `.env` lokal atau environment variable.
- Karena lisensi tidak eksplisit, data kunjungan dipakai terbatas untuk keperluan akademik non-komersial dengan atribusi lengkap.

## Catatan kualitas data
- Kolom `tahun` berisi 2025 (12 bulan) dan 2026 (Januari–Oktober). `TAHUN_DATA` diambil dari tahun yang lengkap 12 bulan, yaitu 2025.
- Nama `'ALUN ALUN SURABAYA BALAI PEMUDA '` punya spasi di ujung, hanya pada 12 baris 2025. Data mentah dibiarkan; `strip()` dilakukan pada salinan, dan jumlah baris yang berubah dicatat.
- Nilai nol adalah data sah (tidak ada kunjungan tercatat), bukan data hilang.
- **Bulan yang diduga disalin.** Kode membandingkan semua pasangan bulan per tahun dan melaporkan pasangan dengan ≥14 dari 16 destinasi identik:
  - Juni dan Juli 2025: identik 16/16.
  - November 2025 sama dengan Juni dan Juli 2025 pada 15/16.
  - September dan Oktober 2026: identik 15/16.

  Bulan yang lebih akhir pada tiap pasangan ditandai `diduga_salinan` di `data/processed/`; nilai di `data/raw/` tidak diubah. Analisis 5.3 diulang dengan dan tanpa bulan bertanda.

## Atribusi
- Data kunjungan wisatawan: Pemerintah Kota Surabaya (penerbit asli), melalui katalog data.go.id (Portal Satu Data Indonesia); berkas dihosting di ckan.surabaya.go.id. Lisensi tidak dicantumkan pada tabel metadata halaman dataset data.go.id; status akses Terbuka.
- Data cuaca: [Open-Meteo.com](https://open-meteo.com/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Tabel kecamatan: kontributor Wikipedia, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
