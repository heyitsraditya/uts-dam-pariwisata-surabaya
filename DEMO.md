# Skrip Demo 5 Menit — UTS DAM Pariwisata Surabaya

Buka `uts_dam.ipynb` yang sudah dieksekusi. Angka dalam kurung siku `[n]` adalah nomor sel kode (*execution count*) yang ditunjukkan. Gulir dari atas ke bawah; urutannya sama dengan urutan soal.

| Waktu | Bagian | Sel | Yang ditunjukkan dan dikatakan |
|---|---|---|---|
| 0:00–0:20 | Judul | (markdown) | "Topik saya kunjungan wisatawan ke 16 destinasi di Kota Surabaya tahun 2025 dan cuaca bulanannya. Tiga sumber: CSV Open Data Surabaya, API Open-Meteo, dan scraping tabel kecamatan Wikipedia." |
| 0:20–0:50 | 0. Setup | [2], [3] | [2]: email kontak dibaca dari env/.env, User-Agent tampil dengan kontak **disamarkan**. [3]: `etis_get()` berisi timeout, jeda per host, retry + *exponential backoff* untuk 429/5xx, dan log status code. Sebut juga `md5_file()` dan `catat_provenance()`. |
| 0:50–1:20 | 1.1 robots & unduh | [4], [5] | robots.txt CKAN: `Disallow: /api/`, `Crawl-delay: 10`. Tabel `can_fetch()`: halaman dataset dan unduhan CSV `True`, CKAN API `False`. Berkas disimpan di `data/raw/`. |
| 1:20–1:50 | 1.2 parameter baca | [6], [7], [8] | Byte mentah: ASCII, tanpa BOM, header berisi 8 `;`. Jadi `sep=";"`, `encoding="utf-8"`, `dtype` eksplisit; `na_values`/`thousands` tidak perlu. Hasil: 352 baris × 9 kolom. |
| 1:50–2:20 | 1.3–1.6 identifikasi | [9]–[14] | Wisnus dan wisman di kolom terpisah; tabulasi bulan × tahun. **TAHUN_DATA = 2025** karena hanya 2025 yang lengkap 12 bulan [12]. Juni = Juli terdeteksi [13]. Estimasi storage ×12×1,3 beserta asumsinya [14]. |
| 2:20–2:50 | 2. Etika | [16], [17], [19] | "No License Provided" dikutip, plus kutipan halaman About (Perpres 39/2019, Perwali 126/2021). Tabel PII per kolom: tidak ada. Checklist 9 butir. Tunjuk markdown 2.3 tentang email pribadi. |
| 2:50–3:30 | 3. API | [20]–[25] | Markdown 3.1: kenapa bukan API CKAN (dilarang robots.txt). Rentang tanggal diturunkan dari data [20]. Satu request, log status [21]. Bukti lisensi CC BY 4.0 [22]. `json_normalize` + DataFrame: **365 baris** harian, lalu 12 baris bulanan [23]–[24]. |
| 3:30–4:00 | 4. Scraping | [26]–[29] | Cuplikan robots.txt Wikipedia dan `can_fetch() = True` [26]. HTML disimpan, `pd.read_html`: 31 kecamatan [27]–[28]. Footer CC BY-SA 4.0 dan atribusi [29]. |
| 4:00–4:40 | 5. Merge | [30]–[35] | Tabel perubahan kunci [30]. Cek kunci unik [31]. `validate="many_to_one"`, `indicator=True`: **192 → 192**, semua `both`, `duplicated().sum() == 0` [32]. Outer join tanpa baris yatim [33]. `gabungan.csv` dan metadata + MD5 [34]–[35]. |
| 4:40–5:00 | 5.3 & 6 | [36]–[40] | Grafik kunjungan vs hujan (indikatif). Provenance 10 baris, verifikasi MD5 ulang `tidak_berubah = True` [39], log request [40]. Tutup dengan: "Semua lulus `scripts/verify_submission.py`." |

---

## 10 pertanyaan yang mungkin ditanyakan dosen

**1. Kenapa ada banyak nilai nol? Apakah itu data hilang?**
Bukan. Nol berarti tidak ada kunjungan tercatat pada destinasi dan bulan itu; misalnya banyak museum memang tidak dikunjungi wisman. Sel kosong tidak ada sama sekali [8]. Di subset 2025 ada 71 nol pada wisman dan 1 pada wisnus. Karena itu `na_values` tidak dipakai: mengubah 0 menjadi NaN justru merusak data.

**2. Kenapa `validate="many_to_one"`?**
Sisi kiri punya 16 baris per bulan (satu per destinasi), sisi kanan tepat satu baris cuaca per bulan. `many_to_one` membuat pandas melempar error jika kunci di sisi kanan ternyata duplikat, karena duplikat seperti itu akan menggandakan baris diam-diam. Buktinya: baris sebelum = sesudah (192), semua `both`, dan `duplicated().sum() == 0`.

**3. Bagaimana kepatuhan robots.txt dan Crawl-delay ditegakkan?**
robots.txt dibaca dengan `urllib.robotparser` dan `can_fetch()` ditampilkan sebelum akses. CKAN Surabaya melarang `/api/`, jadi API-nya tidak dipakai. `Crawl-delay: 10` dibaca dari robots.txt dan dipakai `etis_get()` sebagai jeda minimum ke host itu.

**4. Kenapa Open-Meteo hanya satu titik, bukan per destinasi?**
Semua 16 destinasi berada di dalam satu kota yang jaraknya beberapa kilometer, sedangkan grid reanalisis Open-Meteo berukuran ±9–25 km. Per destinasi hanya akan menghasilkan data yang hampir sama dengan 16 kali request. Satu titik memenuhi minimisasi data dan menghemat kuota API.

**5. Koordinatnya berbeda dengan Wikipedia?**
Titik yang dipakai (-7.2575, 112.7521) adalah pusat kota yang ditetapkan untuk tugas ini. Infobox Wikipedia mencantumkan -7.2463, 112.7378, selisih sekitar 2 km. Perbedaan ini lebih kecil dari ukuran satu sel grid cuaca, sehingga tidak mengubah hasil. Keduanya ditulis terbuka di Soal 3.1.

**6. Juni dan Juli 2025 kok sama persis?**
Sel [13] mendeteksinya otomatis: ke-16 destinasi identik untuk wisnus dan wisman, yang hampir mustahil terjadi alami. Dugaannya kesalahan salin di sumber. Saya melaporkannya di notebook dan `gabungan_metadata.json`, tetapi tidak mengubah data, karena raw harus immutable dan tidak ada dasar untuk menebak angka aslinya.

**7. Lisensinya tidak tercantum, apakah boleh dipakai?**
Halaman dataset menulis "No License Provided", dan itu saya tulis apa adanya. Portal adalah Open Data resmi Pemkot Surabaya (Perwali 126/2021) yang menyatakan data dapat diakses masyarakat secara terbuka. Saya memakainya terbatas untuk akademik, dengan atribusi, tanpa mengklaim lisensi tertentu.

**8. Kenapa email pribadi di User-Agent, bukan email kampus?**
Soal meminta email kampus, tetapi mahasiswa tidak diberi email kampus. Fungsinya agar pemilik situs bisa menghubungi pengakses, dan email pribadi memenuhi fungsi itu. Email dibaca dari `.env` atau environment variable, tidak tertulis di notebook, tidak dicetak, dan tidak di-commit; skrip verifikasi memastikannya.

**9. Kenapa topiknya Surabaya, bukan Bali?**
Rencana awal memang Bali. Saat seleksi, dataset Bali tidak memenuhi syarat dari lingkungan pengerjaan: portal Satu Data Bali mensyaratkan formulir nama dan email untuk unduhan, Data Sektoral Bali memakai login SSO, dataset Denpasar hanya sekitar 12 baris per tahun, dan katalog.data.go.id tidak dapat diakses. Open Data Surabaya menyediakan CSV terbuka lebih dari 100 baris dengan robots.txt yang jelas. Topik tetap sektor pariwisata.

**10. Kenapa tidak memakai API resmi portal sumber seperti yang diminta soal?**
Soal meminta *mengutamakan* API resmi. API CKAN Surabaya ada, tetapi dilarang robots.txt (`Disallow: /api/`). Memakainya berarti melanggar kepatuhan scraping etis, jadi saya memakai alternatif yang disebut soal, yaitu API publik Open-Meteo untuk cuaca di lokasi dataset.

### Cadangan (jika ditanya)
- **Kenapa tabel Wikipedia tidak ikut di-merge?** Data kunjungan tidak punya kolom kecamatan, sehingga tidak ada kunci yang sah. Soal mewajibkan minimal dua sumber, dan merge berkas × API sudah memenuhinya.
- **Bagaimana jika Open-Meteo membalas 429?** `etis_get()` mencoba ulang dengan backoff 2, 4, 8, 16 detik atau sesuai `Retry-After`. Jika kuota harian habis, notebook berhenti dengan pesan jelas dan tidak membanjiri server.
- **Bagaimana menjamin data mentah tidak berubah?** `simpan_mentah()` menolak menimpa berkas. MD5 dihitung ulang di akhir notebook [39] dan oleh `scripts/verify_submission.py`.
