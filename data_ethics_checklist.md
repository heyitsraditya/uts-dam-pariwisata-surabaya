# Data Ethics Checklist — UTS DAM Pariwisata Surabaya

Dihasilkan otomatis oleh `uts_dam.ipynb` (Soal 2). Kolom *bukti* merujuk ke bagian notebook dan berkas di repo.

| No | Butir | Status | Bukti |
|---|---|---|---|
| 1 | Kewenangan penerbit & atribusi | Terpenuhi | Penerbit: Pemerintah Kota Surabaya; katalog: data.go.id; host berkas: ckan.surabaya.go.id. Open-Meteo (CC BY 4.0) dan Wikipedia (CC BY-SA 4.0) juga diatribusi. Bukti: Soal 1.1, provenance. |
| 2 | Lisensi | Terpenuhi dengan catatan | Lisensi tidak dicantumkan di metadata data.go.id (status akses: Terbuka). Pemakaian dibatasi akademik non-komersial dengan atribusi lengkap. Bukti: tabel 2.1, docs/bukti_metadata_data_go_id_2026-11-17.png. |
| 3 | Ketentuan portal | Terpenuhi | data.go.id: akses Terbuka; Open-Meteo: non-komersial dan batas panggilan harian (dikutip di Soal 3); Wikimedia: User-Agent berkontak. Bukti: Soal 2.1, 3. |
| 4 | Kualitas metadata (banner SDI) | Dicatat | Banner SDI dan metadata kosong dicatat; tiga ketidakcocokan katalog vs berkas dan bulan yang diduga disalin ditandai tanpa mengubah raw. Bukti: Soal 1.3, 1.4. |
| 5 | PII / quasi-identifier | Terpenuhi | Tidak ada PII maupun quasi-identifier; data agregat bulanan per destinasi. Bukti: tabel 2.2. |
| 6 | Minimisasi data | Terpenuhi | Satu CSV, satu titik koordinat, variabel cuaca seperlunya, satu halaman Wikipedia; analisis hanya TAHUN_DATA. |
| 7 | robots.txt & rate limit | Terpenuhi | robots.txt CKAN, Open-Meteo, dan Wikipedia dibaca dengan robotparser; /api/ CKAN dilarang sehingga tidak dipakai; Crawl-delay 10 detik ditegakkan; etis_get memakai timeout, jeda, backoff. Bukti: Soal 1.6, 3, 4, log request. |
| 8 | Keamanan kredensial | Terpenuhi | Tidak ada API key/token. Email kampus dibaca dari CONTACT_EMAIL (env/.env); .env di .gitignore, hanya .env.example yang di-commit. Bukti: Setup. |
| 9 | Transparansi & reproducibility | Terpenuhi | Satu notebook end-to-end; provenance.csv; data mentah tidak diubah dengan MD5 diverifikasi ulang; requirements.txt; gabungan_metadata.json. |
