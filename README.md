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
- 🌐 **Modular Provider Architecture (`BaseProvider` & `ProviderRegistry`)**: Dibangun dengan pola *registry/plugin* ala `yt-dlp`. Setiap penyedia terisolasi secara mandiri dan sangat mudah diperluas (*scalable*).
- 🔄 **Cross-Provider Episode Stream Fallback**: Jika seluruh server video pada suatu episode di penyedia A gagal diputar/DMCA, `anindo` tidak akan menyerah, melainkan **otomatis mencari mirror episode yang sama di penyedia cadangan** dan langsung memutarnya secara transparan!
- 🛡️ **Enterprise Resilient Scraper**:
  - **Zero-Regex DOM Tokenizer**: Menggunakan `html.parser` bawaan Python yang kebal terhadap perubahan urutan atribut HTML, penataan spasi, minifikasi HTML, dan perombakan tema web.
  - **Remote OTA Rules (`rules.json`)**: Pola selektor dan rute ekstraksi dikonfigurasi secara jarak jauh lewat GitHub tanpa perlu mengubah kode skrip Python jika web sumber berubah.
  - **Data Contract & Self-Healing**: Memvalidasi integritas data episode dan otomatis melakukan *failover* antar penyedia jika ada struktur data yang rusak.
  - **CI/CD Canary Monitoring**: Diuji otomatis setiap hari via GitHub Actions untuk memastikan scraper dan resolver selalu 100% sehat.
- 🔄 **Dynamic Domain Resolver (Anti-Blokir)**: Dilengkapi sistem deteksi pergantian domain otomatis (auto-probing & follow redirect) dan konfigurasi jarak jauh lewat file `domains.json` di GitHub.
- ⚡ **Pencarian Interaktif & Smart Seek Auto-Resume**:
  - Menggunakan `fzf` untuk navigasi cepat dan mulus.
  - **Monitoring Status Pemutaran Real-Time**: Terhubung ke MPV via JSON IPC untuk mencatat posisi persis tontonan.
  - **Smart Seek Resume**: Jika MPV ditutup di tengah episode (<85%), status ditandai sebagai jeda (`in_progress`) dan menu utama menampilkan `[Lanjut Nonton] Judul - Episode X [Lanjut di MM:SS] (P%)` serta otomatis melanjutkan pemutaran langsung di titik terakhir (`--start`).
  - **Auto-Next Episode**: Jika episode ditonton hingga selesai (≥85%), anindo otomatis menawarkan pemutaran episode berikutnya (`X+1`).
- 📦 **Dukungan Rentang Episode & Batch Download (`-e 1-12`, `-e 1,3,5`, `-e all`)**:
  - Memungkinkan penentuan banyak episode sekaligus untuk unduhan batch berurutan maupun pemutaran bersambung (*autoplay*).
- 🚀 **Akselerasi Download Multi-Connection (`aria2c` / `yt-dlp`)**: Mengunduh video tunggal maupun batch dengan akselerasi hingga 16 koneksi paralel (`-d`).
- ⚙️ **Konfigurasi Preferensi Pengguna (`~/.config/anindo/config.json`)**:
  - Kustomisasi direktori unduhan permanen, penyedia default, kualitas pilihan, bendera MPV khusus, dan notifikasi desktop.
- 🐧 **Integrasi Desktop Linux Native**:
  - **Socket IPC MPV Statis (`/tmp/anindo-mpv.sock`)**: Selalu tersedia selama pemutaran, langsung terbaca oleh widget status bar (Waybar, Caelestia) dan skrip `playerctl`/MPRIS.
  - **Window Title**: `--title="anindo: ${TITLE}"` ramah terhadap *window rules* tiling window manager (Hyprland / Sway).
  - **Desktop Notification**: Notifikasi popup via `notify-send` saat stream mulai diputar atau selesai diunduh.
- 🎯 **Pilihan Kualitas Fleksibel (`-q`)**: Mendukung format fleksibel seperti `-q 720p`, `-q 1080`, `-q best`, lengkap dengan *smart proximity fallback*.
- 🔄 **Pembaruan Mandiri Cepat (`anindo -u`)**: Cek dan perbarui binari langsung ke rilis GitHub terbaru tanpa perlu curl script manual ulang.
- 📺 **Pemutar Video MPV**: Streaming langsung tanpa iklan web atau pop-up, mendukung resume posisi tontonan terakhir.
- 🕒 **Watch State XDG**: Riwayat tontonan disimpan sesuai standar `$XDG_STATE_HOME/anindo/history.json`.
- 🔥 **Anime On-Going**: Akses cepat ke daftar anime yang sedang rilis musim ini (`-o`).

---

## 📦 Kebutuhan Sistem (Dependencies)

Pastikan peralatan berikut sudah terpasang di sistemmu:

- **Python 3** (standar bawaan Linux)
- **mpv** (pemutar video)
- **fzf** (menu interaktif terminal)
- **curl** (pengambil data web)
- **python-cryptography** (untuk dekripsi stream HLS anime klasik)
- **aria2c** *(opsional)*: Untuk akselerasi unduhan hingga 16x lebih cepat
- **yt-dlp** *(opsional)*: Untuk penanganan unduhan HLS m3u8

### Cara Install Dependensi:

* **Arch Linux / Manjaro:**
  ```bash
  sudo pacman -S python python-cryptography mpv fzf curl yt-dlp aria2
  ```
* **Ubuntu / Debian / Linux Mint:**
  ```bash
  sudo apt update && sudo apt install python3 python3-cryptography mpv fzf curl yt-dlp aria2
  ```
* **Fedora:**
  ```bash
  sudo dnf install python3 python3-cryptography mpv fzf curl yt-dlp aria2
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

### 1. Menu Utama Interaktif (Termasuk Smart Auto-Resume)
Jalankan tanpa argumen untuk menampilkan menu pilihan:
```bash
anindo
```
Jika tontonan sebelumnya dijeda, kamu bisa langsung melanjutkan dari menit dan detik terakhir!

### 2. Cari Anime (Modern atau Klasik)
```bash
anindo "initial d"
anindo frieren
anindo "slam dunk"
anindo "one piece"
```

### 3. Tonton Episode atau Rentang Episode (Batch Autoplay)
Gunakan opsi `-e` atau `--episode` dengan angka, rentang, daftar koma, atau `all`:
```bash
anindo "frieren" -e 10           # Tonton episode 10
anindo "frieren" -e 1-5           # Putar berurutan episode 1 s/d 5 (autoplay)
anindo "frieren" -e 1,3,5         # Putar episode 1, 3, dan 5
anindo "frieren" -e all           # Putar seluruh episode berurutan
```

### 4. Mengunduh Video (Single & Batch Download via aria2c)
Tambahkan flag `-d` atau `--download`:
```bash
anindo "solo leveling" -e 1 -d       # Unduh episode 1
anindo "solo leveling" -e 1-12 -d    # Unduh batch episode 1 sampai 12
anindo "solo leveling" -e all -d     # Unduh semua episode dalam seri
```
*Jika dijalankan tanpa `-e`, anindo akan menampilkan menu interaktif dengan opsi `[Unduh Semua Episode (Batch)]`.*

### 5. Tonton Anime On-Going Terbaru
```bash
anindo -o
```

### 6. Lanjutkan Tontonan Terakhir (Resume History)
```bash
anindo -c
```
Atau lihat daftar riwayat lengkap yang pernah ditonton:
```bash
anindo --history
```

### 7. Memilih Sumber Data (Provider)
Secara default mencari di semua penyedia (`all`). Kamu bisa memilih secara spesifik:
```bash
anindo -p nontonanime "initial d"
anindo -p otakudesu "frieren"
```

### 8. Memilih Kualitas Video (Resolusi)
Kualitas default adalah yang tertinggi (`best`). Mendukung penulisan dengan atau tanpa `p`:
```bash
anindo -q 720p "frieren"
anindo -q 480 "naruto"
```

### 9. Pembaruan Mandiri (Self-Update)
Periksa dan perbarui binari `anindo` ke versi rilis GitHub terbaru:
```bash
anindo -u
```

### 10. Periksa & Perbarui Domain Sumber
Jika salah satu situs berganti domain, jalankan:
```bash
anindo --update-domains
```

---

## ⚙️ Konfigurasi Pengguna (`config.json`)

Kamu dapat mengatur preferensi default di berkas `~/.config/anindo/config.json`:

```json
{
  "default_quality": "720p",
  "default_provider": "all",
  "download_dir": "~/Videos/Anime",
  "preferred_downloader": "auto",
  "mpv_flags": [
    "--hwdec=auto",
    "--volume=80"
  ],
  "notify": true
}
```

| Opsi | Tipe | Nilai Default | Keterangan |
| :--- | :--- | :--- | :--- |
| `default_quality` | string | `"best"` | Kualitas video bawaan (`360p`, `480p`, `720p`, `1080p`, `best`) |
| `default_provider` | string | `"all"` | Penyedia default (`all`, `otakudesu`, `nontonanime`) |
| `download_dir` | string | `""` | Folder tujuan unduhan (contoh: `"~/Videos/Anime"`). Jika kosong, disimpan di direktori saat ini |
| `preferred_downloader` | string | `"auto"` | Urutan downloader pilihan (`"auto"`, `"aria2c"`, `"yt-dlp"`, `"curl"`) |
| `mpv_flags` | list / string | `[]` | Argumen flag tambahan yang diteruskan langsung ke MPV |
| `notify` | boolean | `true` | Toggle notifikasi desktop popup melalui `notify-send` |

---

## 🛠️ Opsi Perintah Lengkap

```text
usage: anindo [-h] [-e EPISODE] [-q {360,360p,480,480p,720,720p,1080,1080p,best}]
              [-p {all,otakudesu,nontonanime}] [-o] [-c] [-d] [--history] [-u]
              [--update-domains] [-V] [query]

positional arguments:
  query                 Judul anime yang dicari (misal: 'initial d', 'frieren')

options:
  -h, --help            Tampilkan bantuan dan keluar
  -e, --episode EPISODE Nomor atau rentang episode (misal: -e 10, -e 1-12, -e 1,3,5, -e all)
  -q, --quality         Kualitas video pilihan (360p, 480p, 720p, 1080p, best)
  -p, --provider        Pilih penyedia anime: all, otakudesu, nontonanime
  -o, --ongoing         Pilih dari daftar anime on-going terbaru
  -c, --continue-watch  Lanjutkan anime dari riwayat terakhir (otomatis episode berikutnya)
  -d, --download        Unduh video ke lokal alih-alih memutar (didukung aria2c/yt-dlp)
  --history             Tampilkan riwayat anime yang pernah ditonton
  -u, --update          Periksa dan perbarui anindo ke versi rilis GitHub terbaru
  --update-domains      Segarkan dan periksa domain aktif dari GitHub / resolver
  -V, --version         Tampilkan versi program
```

---

## 📜 Lisensi

[MIT License](LICENSE)
