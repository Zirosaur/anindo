# anindo (Anime Indo CLI)

> CLI streaming anime dengan subtitle bahasa Indonesia langsung di terminal, mirip dengan `ani-cli`.

```
  __ _ _ __ (_)_ __   __| | ___  
 / _` | '_ \| | '_ \ / _` |/ _ \ 
| (_| | | | | | | | | (_| | (_) |
 \__,_|_| |_|_|_| |_|\__,_|\___/ 
 Anime Subtitle Indonesia CLI
```

## ✨ Fitur

- 🇮🇩 **Subtitle Bahasa Indonesia Asli**: Sub Indo sudah tertanam langsung di videonya (hardsub), tidak perlu repot sinkronisasi file `.srt` eksternal.
- 🏎️ **Koleksi Lengkap (Modern + Anime Lawas/Vintage)**: Mendukung anime modern maupun anime klasik tahun 90-an & 2000-an seperti *Initial D (Stage 1-Final)*, *Slam Dunk*, *Great Teacher Onizuka (GTO)*, *Cowboy Bebop*, *Neon Genesis Evangelion*, dll.
- 🌐 **Multi-Provider Search**: Melakukan pencarian paralel ke berbagai penyedia anime Sub Indo (Otakudesu & NontonAnime) secara otomatis.
- ⚡ **Pencarian Interaktif Cepat**: Menggunakan `fzf` untuk memilih anime dan episode dengan navigasi keyboard yang responsif.
- 🔄 **Multi-Server & Auto-Fallback**: Mendukung berbagai server mirror berkecepatan tinggi (Filedon / Cloudflare R2, Pixeldrain, Putarin HLS, YourUpload, ODCloud). Jika satu server DMCA/offline, otomatis beralih ke server cadangan.
- 📺 **Pemutar Video MPV**: Streaming langsung tanpa iklan web atau pop-up, mendukung resume posisi tontonan terakhir.
- ⏭️ **Auto-Next Episode**: Menawarkan pemutaran episode berikutnya secara otomatis setelah episode selesai.
- 🕒 **Riwayat Tontonan (History & Continue)**: Menyimpan riwayat tontonan untuk langsung melanjutkan kapan saja (`-c`).
- 🔥 **Anime On-Going**: Akses cepat ke daftar anime yang sedang rilis musim ini (`-o`).
- 📥 **Opsi Download**: Bisa mengunduh video ke penyimpanan lokal (`-d`).

---

## 📦 Kebutuhan Sistem (Dependencies)

Pastikan peralatan berikut sudah terpasang di sistemmu:

- **Python 3** (standar bawaan Linux)
- **mpv** (pemutar video)
- **fzf** (menu interaktif terminal)
- **curl** (pengambil data web)
- **python-cryptography** (untuk dekripsi stream HLS anime klasik)

### Cara Install Dependensi:

* **Arch Linux / Manjaro:**
  ```bash
  sudo pacman -S python python-cryptography mpv fzf curl yt-dlp
  ```
* **Ubuntu / Debian / Linux Mint:**
  ```bash
  sudo apt update && sudo apt install python3 python3-cryptography mpv fzf curl yt-dlp
  ```
* **Fedora:**
  ```bash
  sudo dnf install python3 python3-cryptography mpv fzf curl yt-dlp
  ```

---

## 🚀 Instalasi

### Cara 1: Satu Baris Perintah (Rekomendasi)
```bash
curl -sL https://raw.githubusercontent.com/Zirosaur/anindo/main/install.sh | bash
```

### Cara 2: Clone Repositori
```bash
git clone https://github.com/Zirosaur/anindo.git
cd anindo
./install.sh
```

### Cara 3: Manual (Tanpa Installer)
Cukup salin berkas `anindo` ke folder bin lokal:
```bash
mkdir -p ~/.local/bin
cp anindo ~/.local/bin/anindo
chmod +x ~/.local/bin/anindo
ln -sf ~/.local/bin/anindo ~/.local/bin/ani-cli-id
```
*(Pastikan `~/.local/bin` sudah terdaftar di `$PATH` shell kamu)*.

---

## 📖 Cara Penggunaan

### 1. Menu Utama Interaktif
Jalankan tanpa argumen untuk menampilkan menu pilihan:
```bash
anindo
```

### 2. Cari Anime (Modern atau Klasik)
```bash
anindo "initial d"
anindo frieren
anindo "slam dunk"
anindo "one piece"
```

### 3. Tonton Episode Tertentu Langsung
Gunakan opsi `-e` atau `--episode`:
```bash
anindo "initial d" -e 1
anindo "frieren" -e 10
anindo "one piece" -e 1177
```

### 4. Tonton Anime On-Going Terbaru
```bash
anindo -o
```

### 5. Lanjutkan Tontonan Terakhir (Resume History)
```bash
anindo -c
```
Atau lihat daftar riwayat yang pernah ditonton:
```bash
anindo --history
```

### 6. Memilih Sumber Data (Provider)
Secara default mencari di semua penyedia (`all`). Kamu bisa memilih secara spesifik:
```bash
anindo -p nontonanime "initial d"
anindo -p otakudesu "frieren"
```

### 7. Memilih Kualitas Video (Resolusi)
Kualitas default adalah yang tertinggi (`best`). Kamu bisa menentukan resolusi pilihan:
```bash
anindo -q 720 "frieren"
anindo -q 480 "naruto"
```
Pilihan kualitas: `360`, `480`, `720`, `1080`, `best`.

### 8. Mengunduh Video (Download)
```bash
anindo -d -e 1 "initial d"
```

---

## 🛠️ Opsi Perintah Lengkap

```text
usage: anindo [-h] [-e EPISODE] [-q {360,480,720,1080,best}]
              [-p {all,otakudesu,nontonanime}] [-o] [-c] [-d] [--history] [-V]
              [query]

positional arguments:
  query                 Judul anime yang dicari (misal: 'initial d', 'frieren')

options:
  -h, --help            Tampilkan bantuan dan keluar
  -e, --episode EPISODE Nomor episode langsung (misal: -e 10)
  -q, --quality         Kualitas video pilihan (default: best)
  -p, --provider        Pilih sumber anime: all, otakudesu, nontonanime (default: all)
  -o, --ongoing         Pilih dari daftar anime on-going terbaru
  -c, --continue-watch  Lanjutkan anime dari riwayat terakhir
  -d, --download        Unduh video ke lokal alih-alih memutar
  --history             Tampilkan riwayat anime yang pernah ditonton
  -V, --version         Tampilkan versi program
```

---

## 📜 Lisensi

[MIT License](LICENSE)
