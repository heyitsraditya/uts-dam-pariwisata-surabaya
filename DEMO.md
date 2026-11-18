# Skrip Demo 5 Menit — UTS DAM Pariwisata Surabaya

Buka `uts_dam.ipynb` yang sudah dieksekusi. Angka dalam kurung siku `[n]` adalah nomor sel kode (*execution count*) yang ditunjukkan. Gulir dari atas ke bawah; urutannya sama dengan urutan soal.

| Waktu | Bagian | Sel | Yang ditunjukkan dan dikatakan |
|---|---|---|---|
| 0:00–0:20 | Judul | (markdown) | "Topik saya kunjungan wisatawan ke 16 destinasi di Kota Surabaya tahun 2025 dan cuaca bulanannya. Tiga sumber: berkas dari data.go.id, API Open-Meteo, dan scraping tabel kecamatan Wikipedia." |
| 0:20–0:45 | 0. Setup | [2], [3] | [2]: email kampus dibaca dari env/.env, dan User-Agent **lengkap** (memuat `mahasiswa@instiki.ac.id`) tampil di output. [3]: `etis_get()` berisi timeout, jeda per host, retry + *exponential backoff* untuk 429/5xx, dan log status code. |
| 0:45–1:15 | 1.1 Sumber utama | [4], [5] | Tabel peran: data.go.id = katalog (diizinkan soal), ckan.surabaya.go.id = host berkas, Pemerintah Kota Surabaya = penerbit asli. Berkas diunduh manual 17 November 2026; MD5 dihitung [5]. |
| 1:15–1:45 | 1.2 Parameter baca | [6]–[8] | Byte mentah: ASCII, tanpa BOM, CRLF, 1 header + 352 baris, 8 `;` di header. Jadi `sep=";"`, `encoding="utf-8"`; kode wilayah dibaca sebagai teks; `na_values`/`thousands`/`skiprows` tidak perlu. |
| 1:45–2:15 | 1.3–1.5 Identifikasi | [10]–[14] | Makna kolom (parafrase definisi portal) [10]. Spasi di ujung nama hanya pada 12 baris 2025 [11]. **Tiga ketidakcocokan katalog vs berkas** [13]. TAHUN_DATA = 2025, nilai nol subset 2025 [14]. |
| 2:15–2:40 | 1.6–1.9 Kualitas & verifikasi | [15], [17], [19] | Pasangan bulan diduga disalin: Juni–Juli 2025 16/16, November 2025 15/16, September–Oktober 2026 15/16 [15]. Estimasi storage [17]. Unduhan ulang dari tautan CKAN: robots.txt dipatuhi, MD5 "identik dengan unduhan manual" [19]. |
| 2:40–3:05 | 2. Etika | [21]–[23] | Lisensi tidak dicantumkan; status akses Terbuka; banner SDI [21]. Tabel PII: tidak ada [22]. Markdown 2.3 tentang isi User-Agent (email kampus). Checklist 9 butir [23]. |
| 3:05–3:40 | 3. API | [24]–[29] | Markdown 3.1: kenapa bukan API CKAN (`/api/` dilarang). Rentang tanggal diturunkan dari data [24], satu request + log status [25], kutipan lisensi Open-Meteo [26]. **365 baris** harian lalu 12 bulanan [27]–[28]. |
| 3:40–4:05 | 4. Scraping | [30]–[33] | robots.txt Wikipedia dan `can_fetch() = True` [30]. `pd.read_html`: 31 kecamatan [31]–[32]. Footer CC BY-SA 4.0 dan atribusi [33]. |
| 4:05–4:40 | 5. Merge | [34]–[39] | Tabel perubahan kunci [34]. Kunci cuaca unik [35]. `validate="many_to_one"`, `indicator=True`: **192 → 192**, semua `both`, `duplicated().sum() == 0` [36]. `gabungan.csv` dengan kolom `diduga_salinan`, metadata + MD5 [38]–[39]. |
| 4:40–5:00 | 5.3 & 6 | [40], [43] | Korelasi dengan dan tanpa bulan bertanda, plus satu kalimat kesimpulan [40]. Verifikasi MD5 ulang: semua `tidak_berubah = True` [43]. Tutup: "Semua lulus `scripts/verify_submission.py`." |

---

## Pertanyaan yang mungkin ditanyakan dosen

**1. Kenapa ada banyak nilai nol? Apakah itu data hilang?**
Bukan. Nol berarti tidak ada kunjungan tercatat pada destinasi dan bulan itu; misalnya banyak museum memang tidak dikunjungi wisman. Sel kosong tidak ada sama sekali [8]. Di subset 2025 ada 71 nol pada wisman dan 1 pada wisnus [14]. Karena itu `na_values` tidak dipakai: mengubah 0 menjadi NaN justru merusak data.

**2. Kenapa `validate="many_to_one"`?**
Sisi kiri punya 16 baris per bulan (satu per destinasi), sisi kanan tepat satu baris cuaca per bulan. `many_to_one` membuat pandas melempar error jika kunci di sisi kanan ternyata ganda, karena kunci ganda akan menggandakan baris diam-diam. Buktinya: baris sebelum = sesudah (192), semua `both`, dan `duplicated().sum() == 0`.

**3. Bagaimana kepatuhan robots.txt dan Crawl-delay ditegakkan?**
robots.txt dibaca dengan `urllib.robotparser` dan `can_fetch()` ditampilkan sebelum akses. ckan.surabaya.go.id melarang `/api/`, jadi API-nya tidak dipakai. Path unduhan `/dataset/.../download/` diizinkan. `Crawl-delay: 10` dibaca dari robots.txt dan dipakai `etis_get()` sebagai jeda minimum ke host itu.

**4. Kenapa Open-Meteo hanya satu titik, bukan per destinasi?**
Semua 16 destinasi berada di dalam satu kota yang jaraknya beberapa kilometer, sedangkan grid reanalisis Open-Meteo berukuran ±9–25 km. Per destinasi hanya akan menghasilkan data yang hampir sama dengan 16 kali request. Satu titik memenuhi minimisasi data dan menghemat kuota.

**5. Koordinatnya berbeda dengan Wikipedia?**
Titik yang dipakai (-7.2575, 112.7521) adalah pusat kota yang ditetapkan untuk tugas ini. Infobox Wikipedia mencantumkan -7.2463, 112.7378, selisih sekitar 2 km. Perbedaan ini lebih kecil dari satu sel grid cuaca, sehingga tidak mengubah hasil. Keduanya ditulis terbuka di Soal 3.1.

**6. Juni dan Juli 2025 kok sama persis?**
Sel [15] membandingkan semua pasangan bulan per tahun:
- Juni dan Juli 2025 identik untuk 16 dari 16 destinasi.
- November 2025 sama dengan keduanya pada 15 dari 16; hanya wisnus JAMBOREE PLAYLAND yang berbeda.
- September dan Oktober 2026 sama pada 15 dari 16.

Kesamaan sebanyak itu hampir mustahil terjadi alami, jadi bulan yang lebih akhir *diduga disalin*. Itu dugaan, bukan fakta. Data mentah tidak diubah; bulan itu hanya ditandai `diduga_salinan` di `data/processed/`. Analisis 5.3 diulang tanpa bulan bertanda untuk melihat apakah kesimpulannya berubah. Oktober 2026 kemungkinan *placeholder* salinan September, dan tidak memengaruhi merge karena yang dipakai hanya 2025.

**7. Kenapa topiknya Surabaya, bukan Bali?**
Rencana awal memang Bali. Saat seleksi, dataset Bali tidak dapat dipakai dari lingkungan pengerjaan:
- Satu Data Bali mensyaratkan formulir nama dan email untuk unduhan.
- Data Sektoral Bali memakai login SSO.
- Dataset Denpasar hanya sekitar 12 baris per tahun.

Dataset kunjungan wisatawan Kota Surabaya terdaftar di data.go.id, punya lebih dari 100 baris, dan tetap di sektor pariwisata.

**8. Apa isi User-Agent dan kenapa?**
Isinya nama klien, tujuan akademik, dan kontak: `UTS-DAM-INSTIKI/1.0 (tugas kuliah Data Acquisition & Management; kontak: mahasiswa@instiki.ac.id) python-requests/<versi>`. Soal mewajibkan User-Agent berisi email kampus agar pemilik situs tahu siapa yang mengakses dan bisa menghubungi bila ada masalah; Wikimedia juga meminta kontak di User-Agent. Email dibaca dari `CONTACT_EMAIL` (`.env` atau environment variable), dan User-Agent lengkapnya dicetak di sel Setup [2] sebagai bukti. `.env` tidak di-commit; yang ada di repo hanya `.env.example`.

**9. Kenapa tidak memakai API resmi portal sumber seperti yang diminta soal?**
Soal meminta *mengutamakan* API resmi. API yang melayani berkas ini adalah CKAN API di host berkas, dan robots.txt host itu menulis `Disallow: /api/` (`can_fetch_api = False` di [19]). Memakainya berarti melanggar kepatuhan, jadi saya memakai alternatif yang disebut soal: API publik Open-Meteo untuk cuaca di lokasi dataset.

**10. Bagaimana menjamin data mentah tidak berubah?**
`simpan_mentah()` menolak menimpa berkas yang sudah ada. MD5 setiap berkas raw dicatat di `provenance.csv`, dihitung ulang di akhir notebook [43], dan diperiksa lagi oleh `scripts/verify_submission.py`. Untuk berkas utama, MD5 juga dibandingkan dengan unduhan ulang dari tautan CKAN [19].

### Latihan: pertanyaan tentang sumber data.go.id

**11. Kenapa sumbernya data.go.id padahal berkasnya dihosting di CKAN?**
Soal mengizinkan berkas dari data.go.id, dan dataset ini saya temukan serta unduh dari halaman data.go.id lewat tombol *Download*. data.go.id adalah katalog nasional (Satu Data Indonesia) yang mencatat metadata, sedangkan berkasnya disimpan oleh penerbit asli, Pemerintah Kota Surabaya, di ckan.surabaya.go.id; tombol *Download* mengarah ke sana dengan Dataset ID yang sama. Ketiganya dicatat terbuka di provenance: katalog, host berkas, dan penerbit asli.

**12. Kenapa label data.go.id berhenti di Agustus 2026 tetapi berkasnya sampai Oktober 2026?**
Metadata di katalog terakhir dimodifikasi 25-09-2026 dan tidak ikut diperbarui, sedangkan berkas di host CKAN diperbarui hingga Oktober 2026. Slug URL `-ta-2025` juga tidak lagi sesuai dengan isinya. Karena itu identitas berkas tidak saya buktikan dengan label katalog, melainkan dengan MD5 dan tanggal unduh. Ketiga ketidakcocokan dihitung dari data di sel [13].

**13. Apa arti banner SDI?**
Halaman menampilkan *"Data berikut ini masih dalam proses pemenuhan Prinsip SDI"*. Artinya dataset belum sepenuhnya memenuhi prinsip Satu Data Indonesia, misalnya standar data, metadata baku, dan kode referensi. Ini terlihat dari tabel metadata yang kosong semua. Saya mencatatnya sebagai catatan kualitas di checklist, dan itulah alasan saya memeriksa sendiri isi berkas (nol, spasi, bulan yang diduga disalin).

**14. Kenapa lisensinya tidak ada?**
Tabel metadata halaman dataset data.go.id tidak memuat kolom lisensi; daftar kolomnya berakhir di "Metode". Yang tercantum hanya status akses "Terbuka". Saya menulisnya apa adanya dan tidak mengarang lisensi. Karena lisensi tidak eksplisit, saya membatasi pemakaian untuk keperluan akademik non-komersial dengan atribusi lengkap kepada Pemerintah Kota Surabaya dan data.go.id. Buktinya ada di tangkapan layar metadata.
