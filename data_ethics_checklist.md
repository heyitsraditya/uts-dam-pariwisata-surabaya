# Data Ethics Checklist — UTS DAM Pariwisata Surabaya

Dihasilkan otomatis oleh `uts_dam.ipynb` (Soal 2.4). Kolom *bukti* merujuk ke bagian notebook dan berkas di repo.

| No | Butir | Status | Bukti |
|---|---|---|---|
| 1 | Sumber & kewenangan penerbit | Terpenuhi | Penerbit: Dinas Kebudayaan, Kepemudaan dan Olah Raga serta Pariwisata (Disbudporapar) Kota Surabaya, melalui portal resmi Open Data Surabaya (ckan.surabaya.go.id; Perwali 126/2021). Cuaca: Open-Meteo. Tabel kecamatan: Wikipedia ID (kode Kemendagri). Bukti: Soal 1.1, 2.1, data/raw/ckan_surabaya_dataset_page.html. |
| 2 | Lisensi | Terpenuhi dengan catatan | Dataset kunjungan: lisensi tidak dicantumkan di metadata CKAN ("No License Provided"), dipakai terbatas untuk akademik dengan atribusi. Open-Meteo: data CC BY 4.0. Wikipedia: CC BY-SA 4.0. Bukti: Soal 2.1, 3.1, 4.3. |
| 3 | Ketentuan layanan portal | Terpenuhi | Halaman About Open Data Surabaya (data terbuka untuk dicari, dilihat, diunduh); ketentuan Open-Meteo (gratis nonkomersial, <10.000 panggilan/hari); kebijakan User-Agent Wikimedia. Bukti: Soal 2.1, 3.1, 4.1. |
| 4 | PII / quasi-identifier | Terpenuhi | Tidak ada PII maupun quasi-identifier; data agregat bulanan per destinasi. Bukti: tabel penilaian per kolom Soal 2.2. |
| 5 | Minimisasi data | Terpenuhi | Hanya satu resource CSV, satu titik koordinat cuaca, variabel cuaca harian seperlunya, dan satu halaman Wikipedia. Analisis hanya memakai TAHUN_DATA; baris tahun lain tetap di raw tetapi tidak diproses. Dataset kandidat lain tidak disimpan. |
| 6 | robots.txt & rate limit | Terpenuhi | robots.txt CKAN & Wikipedia dibaca dengan urllib.robotparser dan can_fetch() ditampilkan; CKAN API (/api/) dilarang sehingga tidak dipakai; Crawl-delay 10 detik ditegakkan; etis_get() memakai timeout, jeda, dan backoff untuk 429/5xx. Bukti: Soal 1.1, 4.1, log request di Ringkasan. |
| 7 | Keamanan kredensial | Terpenuhi | Tidak ada API key/token. Email kontak dibaca dari environment variable atau .env (python-dotenv), tidak pernah dicetak (output menyamarkannya); .env ada di .gitignore; hanya .env.example yang di-commit; scripts/verify_submission.py memastikan nilainya tidak ada di repo maupun output. Bukti: sel Setup, Soal 2.3, .gitignore. |
| 8 | Atribusi / sitasi | Terpenuhi | Atribusi ditulis di README, gabungan_metadata.json, dan Ringkasan: Disbudporapar/Open Data Surabaya, Open-Meteo (CC BY 4.0), Wikipedia kontributor (CC BY-SA 4.0). |
| 9 | Transparansi & reproducibility | Terpenuhi | Satu notebook end-to-end; provenance.csv berisi URL, tanggal akses, lisensi, MD5; data mentah immutable dan MD5 diverifikasi ulang; requirements.txt; gabungan_metadata.json mencatat parameter merge. |
