# Data Ethics Checklist — UTS DAM Pariwisata Surabaya

Dihasilkan otomatis oleh `uts_dam.ipynb` (Soal 2.4). Kolom *bukti* merujuk ke bagian notebook dan berkas di repo.

| No | Butir | Status | Bukti |
|---|---|---|---|
| 1 | Kewenangan penerbit & atribusi | Terpenuhi | Penerbit asli: Pemerintah Kota Surabaya; katalog: data.go.id (Portal Satu Data Indonesia, termasuk sumber yang diizinkan soal); host berkas: ckan.surabaya.go.id. Atribusi menyebut penerbit asli dan katalog; Open-Meteo (CC BY 4.0) dan kontributor Wikipedia (CC BY-SA 4.0) juga diatribusi. Bukti: Soal 1.1, 1.8, 4.3, README. |
| 2 | Lisensi | Terpenuhi dengan catatan | Lisensi tidak dicantumkan pada tabel metadata halaman dataset data.go.id. Status akses di portal: Terbuka. Karena tidak eksplisit, pemakaian dibatasi untuk akademik non-komersial dengan atribusi lengkap. Bukti: Soal 2.1, docs/bukti_metadata_data_go_id_2026-11-17.png. |
| 3 | Ketentuan portal | Terpenuhi | data.go.id menandai dataset berstatus akses Terbuka; ketentuan Open-Meteo (non-komersial, batas panggilan harian) dikutip di Soal 3.1; kebijakan User-Agent Wikimedia dipatuhi dengan UA berkontak. Bukti: Soal 2.1, 3.1, 4.1. |
| 4 | Kualitas metadata (banner SDI) | Dicatat | Banner "Data berikut ini masih dalam proses pemenuhan Prinsip SDI" dan tabel metadata kosong; tiga ketidakcocokan katalog vs berkas dicatat; bulan yang diduga disalin ditandai tanpa mengubah raw. Bukti: Soal 1.4, 1.6, 2.1. |
| 5 | PII / quasi-identifier | Terpenuhi | Tidak ada PII maupun quasi-identifier; data agregat bulanan per destinasi. Bukti: tabel per kolom Soal 2.2. |
| 6 | Minimisasi data | Terpenuhi | Satu berkas CSV, satu titik koordinat cuaca, variabel cuaca seperlunya, dan satu halaman Wikipedia. Analisis hanya memakai TAHUN_DATA; baris tahun lain tetap di raw tetapi tidak diproses. |
| 7 | robots.txt & rate limit | Terpenuhi | robots.txt CKAN, Open-Meteo, dan Wikipedia dibaca dengan urllib.robotparser dan can_fetch() ditampilkan; path /api/ CKAN dilarang sehingga tidak dipakai; Crawl-delay 10 detik ditegakkan; etis_get() memakai timeout, jeda, dan backoff 429/5xx. Bukti: Soal 1.9, 3.1, 4.1, log request di Ringkasan. |
| 8 | Keamanan kredensial | Terpenuhi | Tidak ada API key/token. Email kontak dibaca dari environment variable atau .env, tidak pernah dicetak; .env ada di .gitignore; scripts/verify_submission.py memastikan nilainya tidak ada di repo maupun output. Bukti: Setup, Soal 2.3. |
| 9 | Transparansi & reproducibility | Terpenuhi | Satu notebook end-to-end; provenance.csv (URL, tanggal akses, lisensi, MD5, cara perolehan, bukti); data mentah immutable dengan MD5 diverifikasi ulang; requirements.txt; gabungan_metadata.json mencatat parameter merge. |
