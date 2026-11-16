# Skrip Demo (3–5 menit) — UTS DAM Pariwisata Surabaya

Buka `uts_dam.ipynb` yang sudah dieksekusi. Gulir mengikuti urutan di bawah; setiap langkah menunjuk output yang menjadi bukti.

## 0:00–0:30 — Pembuka dan Setup
- "Topik saya kunjungan wisatawan ke 16 destinasi di Kota Surabaya tahun 2025, digabung dengan cuaca bulanan. Ada tiga sumber: berkas CSV dari Open Data Surabaya, API Open-Meteo, dan scraping tabel kecamatan dari Wikipedia."
- Tunjukkan sel Setup: email kontak dibaca dari `.env` lewat `python-dotenv`, bukan ditulis di kode. Output menampilkan **string User-Agent** sebagai bukti.
- Sebut isi `etis_get()`: timeout, User-Agent, jeda per host, retry dengan *exponential backoff* untuk 429/5xx, dan log status code.

## 0:30–1:30 — Soal 1: berkas
- Tunjukkan output `robots.txt` CKAN Surabaya: `/api/` dilarang dan `Crawl-delay: 10`. Tabel `can_fetch()` menunjukkan halaman dataset dan URL unduhan **True**, sedangkan CKAN API **False**. "Karena itu saya tidak memakai API CKAN."
- Pemeriksaan byte mentah: ASCII, tanpa BOM, CRLF, header berisi 8 titik koma. Inilah dasar `sep=";"` dan `encoding="utf-8"`. `na_values` dan `thousands` tidak dipakai karena tidak ada sel kosong maupun pemisah ribuan. Nilai 0 adalah data sah.
- Identifikasi: 352 baris × 9 kolom, terstruktur, wisnus dan wisman di kolom terpisah, satuan orang per bulan.
- **`TAHUN_DATA` diambil dari data:** 2025 lengkap 12 bulan, 2026 hanya 10 bulan, jadi dipakai 2025 (192 baris).
- Temuan kualitas: angka Juni = Juli untuk semua destinasi. Dilaporkan, tidak dikoreksi.
- Estimasi storage: ukuran × 12 × 1,3, asumsinya tertulis di markdown.

## 1:30–2:15 — Soal 2: etika
- Kutipan blok lisensi: "No License Provided". Ditulis apa adanya; halaman About portal dikutip (Perpres 39/2019, Perwali 126/2021, "dapat diakses oleh masyarakat secara terbuka").
- Tabel PII per kolom: tidak ada PII maupun quasi-identifier, karena datanya agregat.
- Checklist 9 butir, juga tersimpan di `data_ethics_checklist.md`.

## 2:15–3:00 — Soal 3: API
- Rentang Open-Meteo diturunkan otomatis dari bulan di data kunjungan (2025-01-01 s.d. 2025-12-31). Satu request untuk satu titik.
- JSON mentah tersimpan di `data/raw/`. `json_normalize` dipakai untuk metadata dan `DataFrame` untuk deret harian, menghasilkan **365 baris** (≥30), lalu diagregasi menjadi 12 baris bulanan.

## 3:00–3:40 — Soal 4: scraping
- Cuplikan `robots.txt` Wikipedia dan `can_fetch(USER_AGENT, WIKI_URL) = True`. Halaman edit (`/w/`) bernilai False.
- HTML mentah disimpan, tabel diambil dengan `pd.read_html`, menghasilkan 31 kecamatan dan 153 kelurahan. Footer lisensi CC BY-SA 4.0 dikutip dan atribusi ditulis.

## 3:40–4:40 — Soal 5: merge
- Tabel perubahan kunci: `strip()` nama destinasi, nama bulan ke angka, filter tahun, agregasi harian ke bulanan.
- Pemeriksaan sebelum merge: kunci cuaca unik, tidak ada duplikat destinasi × bulan.
- `pd.merge(..., on="bulan", validate="many_to_one", indicator=True)` memberi **192 baris sebelum = 192 sesudah**, `_merge` semuanya `both`, dan `duplicated().sum() == 0`.
- Output `gabungan.csv` dan `gabungan_metadata.json` (sumber, kunci, validate, tanggal proses, MD5).
- Grafik kunjungan vs curah hujan; korelasi hanya indikatif (12 titik).

## 4:40–5:00 — Penutup
- Tabel provenance (URL, tanggal akses, lisensi, MD5) dan **verifikasi MD5 ulang**: semua berkas raw `tidak_berubah = True`.
- Log request: semua status code tercatat.

---

## Kemungkinan pertanyaan dosen

**1. Kenapa tidak pakai API CKAN, padahal lebih mudah?**
`robots.txt` portal menulis `Disallow: /api/`. Notebook membuktikannya dengan `can_fetch()` = False, jadi saya hanya memakai halaman dataset dan URL unduhan yang diizinkan, dengan jeda 10 detik sesuai `Crawl-delay`.

**2. Datanya kan berjudul "Tahun 2025", kenapa ada 2026?**
Resource yang terbaru (`...-2026.csv`) berisi Januari 2025 s.d. Oktober 2026. Saya tidak berasumsi: `TAHUN_DATA` dihitung dari kolom `tahun`, yaitu tahun yang lengkap 12 bulan. Baris 2026 tetap ada di raw, hanya tidak dianalisis.

**3. Kenapa `validate="many_to_one"`?**
Sisi kiri punya 16 baris per bulan (satu per destinasi), sisi kanan tepat satu baris cuaca per bulan. `many_to_one` membuat pandas melempar error jika kunci di sisi kanan ternyata duplikat. Duplikat seperti itu akan menggandakan baris diam-diam.

**4. Bagaimana membuktikan tidak ada duplikasi?**
Jumlah baris sebelum (192) = sesudah (192), `indicator=True` menunjukkan semua `both`, `duplicated().sum() == 0`, dan pengecekan *outer join* tidak menemukan bulan yang tidak cocok.

**5. Lisensinya tidak ada, apakah boleh dipakai?**
Lisensi tidak dicantumkan, dan itu saya tulis apa adanya. Portal adalah portal resmi Open Data pemerintah kota yang menyatakan data dapat diakses masyarakat secara terbuka (dasar Perwali 126/2021). Saya memakainya terbatas untuk akademik, dengan atribusi, dan tanpa mengklaim lisensi tertentu.

**6. Apa yang terjadi jika Open-Meteo membalas 429?**
`etis_get()` mengulang dengan backoff 2, 4, 8, 16 detik, atau sesuai `Retry-After`. Jika pesan 429-nya "Daily API request limit exceeded", kuota harian per IP habis, sehingga setelah retry habis notebook berhenti dengan pesan jelas dan tidak membanjiri server.

**7. Bagaimana menjamin data mentah tidak berubah?**
`simpan_mentah()` menolak menimpa berkas yang sudah ada. Saat dijalankan ulang, notebook memakai salinan yang ada. Di akhir, MD5 setiap berkas raw dihitung ulang dan dibandingkan dengan `provenance.csv`.

**8. Kenapa tabel Wikipedia tidak ikut di-merge?**
Data kunjungan tidak punya kolom kecamatan, sehingga tidak ada kunci yang sah. Memetakan destinasi ke kecamatan secara manual akan menambah asumsi yang tidak berasal dari sumber. Tabel itu dipakai untuk mendemonstrasikan kepatuhan robots.txt dan scraping (Soal 4).

**9. Juni dan Juli kok sama persis?**
Notebook mendeteksinya otomatis: ke-16 destinasi identik untuk wisnus dan wisman. Ini dugaan kesalahan salin di sumber. Saya melaporkannya sebagai keterbatasan dan tidak mengubahnya, karena tidak ada dasar untuk menebak angka sebenarnya.

**10. Koordinatnya dari mana?**
Titik pusat Kota Surabaya (-7.2575, 112.7521) ditetapkan untuk tugas ini. Infobox Wikipedia mencantumkan -7.2463, 112.7378, sekitar 2 km dari titik itu. Pada resolusi grid reanalisis Open-Meteo (±9–25 km) perbedaan ini tidak berarti.

**11. Kenapa User-Agent memakai email pribadi?**
Email kampus tidak tersedia. Yang penting pemilik situs bisa menghubungi pengakses. Kebijakan User-Agent Wikimedia meminta kontak, dan saat pengujian, request dengan UA tanpa kontak sempat dibalas 429. Email hanya disimpan di `.env` lokal, yang tidak di-commit.
