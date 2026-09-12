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

- 🇮🇩 **Subtitle Bahasa Indonesia Asli**: Sub Indo sudah tertanam langsung di videonya (hardsub/softsub), tidak perlu repot sinkronisasi subtitle eksternal.
- ⚡ **Pencarian Interaktif Cepat**: Menggunakan `fzf` untuk memilih anime dan episode dengan navigasi keyboard.
- 🔄 **Multi-Server & Auto-Fallback**: Mendukung berbagai server mirror berkecepatan tinggi (Filedon / Cloudflare R2, Pixeldrain, ODCloud). Jika satu server gagal atau terkena blokir DMCA (HTTP 451), otomatis berpindah ke server alternatif.
- 📺 **Pemutar Video MPV**: Streaming langsung tanpa iklan, tanpa browser, mendukung resume posisi tontonan terakhir.
- ⏭️ **Auto-Next Episode**: Menanyakan otomatis pemutaran episode berikutnya setelah episode selesai.
- 🕒 **Riwayat Tontonan (History & Continue)**: Menyimpan episode terakhir yang ditonton untuk melanjutkan kapan saja (`-c`).
- 🔥 **Anime On-Going**: Akses cepat ke daftar anime yang sedang rilis pekan ini (`-o`).
- 📥 **Opsi Download**: Bisa mengunduh video ke penyimpanan lokal (`-d`).

---

## 📦 Kebutuhan Sistem (Dependencies)

Pastikan peralatan berikut sudah terpasang di sistemmu:

- **Python 3** (standar bawaan Linux)
- **mpv** (pemutar video)
- **fzf** (menu interaktif terminal)
- **curl** (pengambil data web)

### Cara Install Dependensi:

* **Arch Linux / Manjaro:**
  ```bash
  sudo pacman -S python mpv fzf curl
  ```
* **Ubuntu / Debian / Linux Mint:**
  ```bash
  sudo apt update && sudo apt install python3 mpv fzf curl
  ```
* **Fedora:**
  ```bash
  sudo dnf install python3 mpv fzf curl
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

### Cara 2: Manual (Tanpa Installer)
Cukup salin berkas `anindo` ke folder bin lokal:
```bash
mkdir -p ~/.local/bin
cp anindo ~/.local/bin/anindo
chmod +x ~/.local/bin/anindo
ln -sf ~/.local/bin/anindo ~/.local/bin/ani-cli-id
```
*(Pastikan `~/.local/bin` sudah ada di `$PATH` shell kamu)*.

---

## 📖 Cara Penggunaan

### 1. Menu Utama Interaktif
Jalankan tanpa argumen untuk menampilkan menu pilihan:
```bash
anindo
```

### 2. Cari Anime Berdasarkan Judul
```bash
anindo frieren
anindo "jujutsu kaisen"
anindo "one piece"
```

### 3. Tonton Episode Tertentu Langsung
Gunakan opsi `-e` atau `--episode`:
```bash
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
Atau lihat daftar riwayat:
```bash
anindo --history
```

### 6. Memilih Kualitas Video (Resolusi)
Kualitas default adalah yang tertinggi (`best`). Kamu bisa menentukan resolusi pilihan:
```bash
anindo -q 720 "frieren"
anindo -q 480 "naruto"
```
Pilihan kualitas: `360`, `480`, `720`, `1080`, `best`.

### 7. Mengunduh Video (Download)
```bash
anindo -d -e 1 "frieren"
```

---

## 🛠️ Opsi Perintah Lengkap

```text
usage: anindo [-h] [-e EPISODE] [-q {360,480,720,1080,best}] [-o] [-c] [-d] [--history] [-V] [query]

positional arguments:
  query                 Judul anime yang dicari

options:
  -h, --help            Tampilkan bantuan dan keluar
  -e, --episode EPISODE Nomor episode langsung (misal: -e 10)
  -q, --quality         Kualitas video pilihan (default: best)
  -o, --ongoing         Pilih dari daftar anime on-going terbaru
  -c, --continue-watch  Lanjutkan anime dari riwayat terakhir
  -d, --download        Unduh video ke lokal alih-alih memutar
  --history             Tampilkan riwayat anime yang pernah ditonton
  -V, --version         Tampilkan versi program
```

---

## 📜 Lisensi

[MIT License](LICENSE)
