"""Verifikasi kelengkapan dan kebersihan submisi UTS DAM setelah notebook dieksekusi.

Cara pakai (dari root repo):
    python scripts/verify_submission.py

Setiap pemeriksaan mencetak LULUS atau GAGAL. Kode keluar 0 jika semua lulus, 1 jika ada yang gagal.
Nilai CONTACT_EMAIL hanya dibandingkan di memori dan TIDAK PERNAH dicetak.
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "uts_dam.ipynb"
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
BARIS_MERGE_DIHARAPKAN = 192

hasil = []  # daftar (nama pemeriksaan, lulus?, keterangan)


def catat(nama, lulus, keterangan=""):
    """Simpan hasil satu pemeriksaan."""
    hasil.append((nama, bool(lulus), keterangan))


def md5_file(path):
    """Hitung MD5 berkas secara bertahap."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for blok in iter(lambda: f.read(65536), b""):
            h.update(blok)
    return h.hexdigest()


def git_ls_files(*args):
    """Daftar berkas yang ter-track git (relatif terhadap root repo)."""
    keluaran = subprocess.run(["git", "ls-files", *args], cwd=ROOT, capture_output=True, text=True, check=True)
    return [baris for baris in keluaran.stdout.splitlines() if baris]


def baca_contact_email():
    """Ambil CONTACT_EMAIL dari environment variable, atau dari .env jika env kosong. Tidak dicetak."""
    nilai = os.environ.get("CONTACT_EMAIL", "").strip()
    if not nilai and (ROOT / ".env").exists():
        for baris in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if baris.strip().startswith("CONTACT_EMAIL="):
                nilai = baris.split("=", 1)[1].strip().strip("'\"")
    return nilai


# ---------------------------------------------------------------- 1. Notebook
nb = None
try:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    sel_kode = [c for c in nb["cells"] if c["cell_type"] == "code"]
    nomor = [c.get("execution_count") for c in sel_kode]
    berurutan = nomor == list(range(1, len(sel_kode) + 1))
    catat("Notebook: semua sel kode dieksekusi dengan execution_count berurutan", berurutan,
          f"{len(sel_kode)} sel kode; nomor pertama yang tidak sesuai: "
          f"{next((n for i, n in enumerate(nomor, 1) if n != i), '-')}")
    sel_error = [n for c, n in zip(sel_kode, nomor)
                 if any(o.get("output_type") == "error" for o in c.get("outputs", []))]
    catat("Notebook: tidak ada output error", not sel_error, f"sel error: {sel_error or 'tidak ada'}")
    sel_kosong = [n for c, n in zip(sel_kode, nomor) if not c.get("outputs")]
    catat("Notebook: setiap sel kode punya output tersimpan", not sel_kosong,
          f"sel tanpa output: {sel_kosong or 'tidak ada'}")
except (OSError, json.JSONDecodeError, KeyError) as err:
    catat("Notebook: dapat dibaca", False, str(err))

# ---------------------------------------------------------------- 2. Merge
try:
    meta = json.loads((PROCESSED_DIR / "gabungan_metadata.json").read_text(encoding="utf-8"))
    sebelum, sesudah = meta.get("baris_sebelum_merge"), meta.get("baris_sesudah_merge")
    catat("Merge: baris sebelum = sesudah = 192",
          sebelum == sesudah == BARIS_MERGE_DIHARAPKAN, f"sebelum {sebelum}, sesudah {sesudah}")
    catat("Merge: semua baris _merge == 'both' dan validate many_to_one",
          meta.get("status_merge", {}).get("both") == sesudah and meta.get("validate") == "many_to_one",
          f"status_merge {meta.get('status_merge')}, validate {meta.get('validate')}")
    with open(PROCESSED_DIR / "gabungan.csv", encoding="utf-8", newline="") as f:
        baris = [tuple(r) for r in csv.reader(f)][1:]
    duplikat = len(baris) - len(set(baris))
    catat("Merge: gabungan.csv berisi 192 baris dan duplicated().sum() == 0",
          len(baris) == BARIS_MERGE_DIHARAPKAN and duplikat == 0, f"{len(baris)} baris, {duplikat} duplikat")
    catat("Merge: MD5 gabungan.csv cocok dengan gabungan_metadata.json",
          meta.get("md5") == md5_file(PROCESSED_DIR / "gabungan.csv"))
except (OSError, json.JSONDecodeError) as err:
    catat("Merge: berkas hasil tersedia", False, str(err))

# ---------------------------------------------------------------- 3. Provenance
try:
    with open(ROOT / "provenance.csv", encoding="utf-8", newline="") as f:
        prov = list(csv.DictReader(f))
    wajib = ["url", "tanggal_akses", "lisensi", "md5", "path_lokal"]
    tidak_lengkap = [p.get("sumber_id") for p in prov if any(not (p.get(k) or "").strip() for k in wajib)]
    catat("Provenance: setiap baris punya URL, tanggal akses, lisensi, MD5", prov and not tidak_lengkap,
          f"{len(prov)} baris; tidak lengkap: {tidak_lengkap or 'tidak ada'}")
    tidak_cocok = [p["sumber_id"] for p in prov
                   if not (ROOT / p["path_lokal"]).exists() or md5_file(ROOT / p["path_lokal"]) != p["md5"]]
    catat("Provenance: MD5 cocok dengan berkas di data/raw", prov and not tidak_cocok,
          f"tidak cocok/hilang: {tidak_cocok or 'tidak ada'}")
    tercatat = {p["path_lokal"] for p in prov}
    berkas_raw = {str(p.relative_to(ROOT)) for p in RAW_DIR.iterdir()
                  if p.is_file() and p.name != ".gitkeep" and not p.name.endswith(".akses")}
    catat("Provenance: setiap berkas di data/raw tercatat", berkas_raw <= tercatat,
          f"belum tercatat: {sorted(berkas_raw - tercatat) or 'tidak ada'}")
    akses_beda = [p["sumber_id"] for p in prov
                  if (ROOT / (p["path_lokal"] + ".akses")).exists()
                  and (ROOT / (p["path_lokal"] + ".akses")).read_text(encoding="utf-8").strip() != p["tanggal_akses"]]
    catat("Provenance: tanggal akses sama dengan catatan *.akses saat unduh", not akses_beda,
          f"berbeda: {akses_beda or 'tidak ada'}")
except (OSError, KeyError) as err:
    catat("Provenance: provenance.csv tersedia", False, str(err))

# ---------------------------------------------------------------- 4. Berkas wajib
wajib_ada = ["uts_dam.ipynb", "README.md", "DEMO.md", "data_ethics_checklist.md", "provenance.csv",
             "requirements.txt", ".env.example", ".gitignore", "data/processed/gabungan.csv",
             "data/processed/gabungan_metadata.json"]
hilang = [b for b in wajib_ada if not (ROOT / b).exists()]
catat("Berkas keluaran wajib tersedia", not hilang, f"hilang: {hilang or 'tidak ada'}")

# ---------------------------------------------------------------- 5. Kebersihan rahasia
try:
    tracked = git_ls_files()
    catat(".env tidak ter-track git", ".env" not in tracked)
    belum_track = [b for b in git_ls_files("--others", "--exclude-standard")
                   if b.startswith("data/") or b in wajib_ada]
    catat("Semua keluaran sudah ter-track git (siap commit)", not belum_track,
          f"belum di-git add: {belum_track[:8] or 'tidak ada'}")

    email = baca_contact_email()
    if not email:
        catat("CONTACT_EMAIL tidak muncul di repo maupun output notebook", False,
              "CONTACT_EMAIL kosong di environment dan .env, sehingga tidak bisa diperiksa")
    else:
        target = email.lower().encode("utf-8")
        bocor = [b for b in tracked if (ROOT / b).is_file() and target in (ROOT / b).read_bytes().lower()]
        if NOTEBOOK.exists() and target in NOTEBOOK.read_bytes().lower() and "uts_dam.ipynb" not in bocor:
            bocor.append("uts_dam.ipynb")
        # Hanya nama berkas yang dicetak, tidak pernah nilai email
        catat("CONTACT_EMAIL tidak muncul di repo maupun output notebook", not bocor,
              f"ditemukan di: {bocor or 'tidak ada'} (nilai tidak dicetak; panjang {len(email)} karakter)")
except (OSError, subprocess.CalledProcessError) as err:
    catat("Git: repo dapat diperiksa", False, str(err))

# ---------------------------------------------------------------- Laporan
lebar = max(len(n) for n, _, _ in hasil)
for nama, lulus, ket in hasil:
    print(f"[{'LULUS' if lulus else 'GAGAL'}] {nama.ljust(lebar)}  {ket}")
jumlah_gagal = sum(not lulus for _, lulus, _ in hasil)
print(f"\nRingkasan: {len(hasil) - jumlah_gagal} LULUS, {jumlah_gagal} GAGAL")
sys.exit(1 if jumlah_gagal else 0)
