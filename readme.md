Domain & IP Resolver

Alat Python sederhana namun kuat untuk melakukan resolusi domain ke IP dan Reverse IP Lookup secara massal menggunakan teknik multithreading.

## ✨ Fitur Utama
- **Auto-Detection**: Mengenali format IP atau Domain secara otomatis.
- **Reverse IP Lookup**: Mengambil data dari RapidDNS, HackerTarget, dan SiteDossier.
- **Multithreading**: Performa tinggi dengan jumlah thread yang dapat diatur pengguna.
- **Data Cleaner**: Membersihkan URL dari protokol (http/https) dan path secara otomatis.
- **Deduplikasi**: Menghasilkan daftar unik tanpa ada data ganda.

## 🛠️ Persyaratan
- Python 3.x
- Library `requests` (Instal via pip: `pip install requests`)

## 🚀 Cara Penggunaan
1. Letakkan file `tools-url.py` dalam satu folder dengan daftar target Anda.
2. Buat file input (misal: `list.txt`) berisi daftar IP atau Domain.
3. Jalankan script melalui Terminal/CMD:
   ```bash
   python tools-url.py
Masukkan nama file input dan tentukan jumlah thread (Rekomendasi: 10-50).

Hasil akan disimpan dalam file hasil_recon_[timestamp].txt.

⚠️ Catatan Keamanan
Alat ini dibuat untuk tujuan penelitian keamanan (Security Research) dan Bug Bounty. Harap gunakan dengan bijak dan patuhi kebijakan privasi dari penyedia API yang digunakan.
**Apakah Anda ingin saya tambahkan fitur untuk mengecek "Status HTTP" agar Anda tahu website mana yang benar-benar aktif (Live) di daftar hasil tersebut?**
