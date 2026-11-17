"""Verifikasi kelengkapan dan kebersihan submisi UTS DAM setelah notebook dieksekusi.

Cara pakai (dari root repo):
    python scripts/verify_submission.py

Setiap pemeriksaan mencetak LULUS, GAGAL, atau PERINGATAN. Kode keluar 0 jika tidak ada GAGAL, 1 jika ada.
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
BERKAS_UTAMA = RAW_DIR / "banyaknya-wisman-wisnus-2026.csv"
BUKTI_PNG = ROOT / "docs" / "bukti_metadata_data_go_id_2026-11-17.png"
TANGGAL_AKSES_UTAMA = "2026-11-17"
PLACEHOLDER = "[ISI SEBELUM KUMPUL]"
BARIS_MERGE_DIHARAPKAN = 192

hasil = []  # daftar (status, nama pemeriksaan, keterangan)


def catat(nama, lulus, keterangan="", peringatan=False):
    """Simpan hasil satu pemeriksaan: LULUS, GAGAL, atau PERINGATAN (tidak menggagalkan)."""
    status = "LULUS" if lulus else ("PERINGATAN" if peringatan else "GAGAL")
    hasil.append((status, nama, keterangan))


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
try:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    sel_kode = [c for c in nb["cells"] if c["cell_type"] == "code"]
    nomor = [c.get("execution_count") for c in sel_kode]
    catat("Notebook: semua sel kode dieksekusi dengan execution_count berurutan",
          nomor == list(range(1, len(sel_kode) + 1)),
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
    catat("Provenance: setiap baris punya URL, tanggal akses, lisensi, MD5", bool(prov) and not tidak_lengkap,
          f"{len(prov)} baris; tidak lengkap: {tidak_lengkap or 'tidak ada'}")
    tidak_cocok = [p["sumber_id"] for p in prov
                   if not (ROOT / p["path_lokal"]).exists() or md5_file(ROOT / p["path_lokal"]) != p["md5"]]
    catat("Provenance: MD5 cocok dengan berkas di data/raw", bool(prov) and not tidak_cocok,
          f"tidak cocok/hilang: {tidak_cocok or 'tidak ada'}")
    tercatat = {p["path_lokal"] for p in prov}
    berkas_raw = {str(p.relative_to(ROOT)) for p in RAW_DIR.rglob("*")
                  if p.is_file() and p.name != ".gitkeep" and not p.name.endswith(".akses")}
    catat("Provenance: setiap berkas di data/raw (termasuk subfolder) tercatat", berkas_raw <= tercatat,
          f"belum tercatat: {sorted(berkas_raw - tercatat) or 'tidak ada'}")
    akses_beda = [p["sumber_id"] for p in prov
                  if (ROOT / (p["path_lokal"] + ".akses")).exists()
                  and (ROOT / (p["path_lokal"] + ".akses")).read_text(encoding="utf-8").strip() != p["tanggal_akses"]]
    catat("Provenance: tanggal akses sama dengan catatan *.akses saat unduh", not akses_beda,
          f"berbeda: {akses_beda or 'tidak ada'}")

    # Sumber utama: data.go.id, tanggal akses 17 November 2026, MD5 cocok dengan berkas data.go.id
    utama = [p for p in prov if p["path_lokal"] == str(BERKAS_UTAMA.relative_to(ROOT))]
    if not utama:
        catat("Provenance: baris sumber utama data.go.id ada", False, f"tidak ada baris untuk {BERKAS_UTAMA.name}")
    else:
        u = utama[0]
        catat("Provenance: sumber utama memuat domain data.go.id dan tanggal 17 November 2026",
              "data.go.id" in u.get("url", "") and TANGGAL_AKSES_UTAMA in u.get("tanggal_akses", ""),
              f"url berisi data.go.id: {'data.go.id' in u.get('url', '')}; tanggal_akses: {u.get('tanggal_akses')}")
        catat("Provenance: MD5 berkas data.go.id cocok dengan provenance.csv",
              BERKAS_UTAMA.exists() and md5_file(BERKAS_UTAMA) == u.get("md5"),
              f"berkas ada: {BERKAS_UTAMA.exists()}")
except (OSError, KeyError) as err:
    catat("Provenance: provenance.csv tersedia", False, str(err))

# ---------------------------------------------------------------- 4. Berkas wajib, placeholder, dan bukti
wajib_ada = ["uts_dam.ipynb", "README.md", "DEMO.md", "data_ethics_checklist.md", "provenance.csv",
             "requirements.txt", ".env.example", ".gitignore", "data/processed/gabungan.csv",
             "data/processed/gabungan_metadata.json", str(BERKAS_UTAMA.relative_to(ROOT))]
hilang = [b for b in wajib_ada if not (ROOT / b).exists()]
catat("Berkas keluaran wajib tersedia", not hilang, f"hilang: {hilang or 'tidak ada'}")

berkas_placeholder = ["provenance.csv", "README.md", "DEMO.md", "data_ethics_checklist.md", "uts_dam.ipynb"]
masih_kosong = [b for b in berkas_placeholder
                if (ROOT / b).exists() and PLACEHOLDER in (ROOT / b).read_text(encoding="utf-8")]
catat(f"Tidak ada '{PLACEHOLDER}' yang tersisa", not masih_kosong, f"masih ada di: {masih_kosong or 'tidak ada'}")

def teks_output_notebook():
    """Gabungkan teks OUTPUT sel kode saja (kode sumber sendiri memuat kata kunci yang dicari)."""
    try:
        sel = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    except (OSError, json.JSONDecodeError, KeyError):
        return ""
    potongan = []
    for c in sel:
        for o in c.get("outputs", []):
            for isi in [o.get("text", "")] + list(o.get("data", {}).values()):
                potongan.append("".join(isi) if isinstance(isi, list) else str(isi))
    return "\n".join(potongan)


frasa_hilang = []
if (ROOT / "provenance.csv").exists() and "TIDAK DITEMUKAN" in (ROOT / "provenance.csv").read_text(encoding="utf-8"):
    frasa_hilang.append("provenance.csv")
if "TIDAK DITEMUKAN" in teks_output_notebook():
    frasa_hilang.append("uts_dam.ipynb (output)")
catat("Frasa bukti lisensi/ketentuan Open-Meteo ditemukan di halaman asli", not frasa_hilang,
      f"ada frasa 'TIDAK DITEMUKAN' di: {frasa_hilang or 'tidak ada'} (periksa halaman secara manual)",
      peringatan=True)

catat("Bukti tangkapan layar metadata data.go.id tersedia", BUKTI_PNG.exists(),
      f"{BUKTI_PNG.relative_to(ROOT)} {'ada' if BUKTI_PNG.exists() else 'belum ditambahkan'}", peringatan=True)

# ---------------------------------------------------------------- 5. Kebersihan rahasia dan git
try:
    tracked = git_ls_files()
    catat(".env tidak ter-track git", ".env" not in tracked)
    belum_track = [b for b in git_ls_files("--others", "--exclude-standard")
                   if b.startswith("data/") or b.startswith("docs/") or b in wajib_ada]
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
lebar = max(len(n) for _, n, _ in hasil)
for status, nama, ket in hasil:
    print(f"[{status:<10}] {nama.ljust(lebar)}  {ket}")
jumlah = {s: sum(h[0] == s for h in hasil) for s in ("LULUS", "GAGAL", "PERINGATAN")}
print(f"\nRingkasan: {jumlah['LULUS']} LULUS, {jumlah['GAGAL']} GAGAL, {jumlah['PERINGATAN']} PERINGATAN")
sys.exit(1 if jumlah["GAGAL"] else 0)
