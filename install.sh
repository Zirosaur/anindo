#!/bin/sh
# Installer script for anindo
set -e

C_RESET="\033[0m"
C_BOLD="\033[1m"
C_BLUE="\033[1;34m"
C_GREEN="\033[1;32m"
C_YELLOW="\033[1;33m"
C_RED="\033[1;31m"
C_CYAN="\033[1;36m"

printf "${C_CYAN}${C_BOLD}"
cat << "EOF"
  __ _ _ __ (_)_ __   __| | ___  
 / _` | '_ \| | '_ \ / _` |/ _ \ 
| (_| | | | | | | | | (_| | (_) |
 \__,_|_| |_|_|_| |_|\__,_|\___/ 
 Anime Subtitle Indonesia CLI
EOF
printf "${C_RESET}\n"

# Check dependencies
printf "${C_BLUE}==>${C_RESET} Memeriksa dependensi sistem...\n"

missing=""
command -v python3 >/dev/null 2>&1 || missing="$missing python3"
command -v curl >/dev/null 2>&1 || missing="$missing curl"
command -v mpv >/dev/null 2>&1 || missing="$missing mpv"
command -v fzf >/dev/null 2>&1 || missing="$missing fzf"

if [ -n "$missing" ]; then
    printf "${C_YELLOW}[PERINGATAN]${C_RESET} Dependensi berikut belum terpasang:%s\n" "$missing"
    printf "Silakan pasang melalui package manager sistemmu:\n"
    printf "  - Arch Linux: sudo pacman -S%s\n" "$missing"
    printf "  - Ubuntu/Debian: sudo apt install%s\n" "$missing"
    printf "  - Fedora: sudo dnf install%s\n\n" "$missing"
fi

# Determine target directory
TARGET_DIR="$HOME/.local/bin"
if [ "$(id -u)" -eq 0 ]; then
    TARGET_DIR="/usr/local/bin"
fi

mkdir -p "$TARGET_DIR"

SCRIPT_SRC="$(dirname "$0")/anindo"
if [ ! -f "$SCRIPT_SRC" ]; then
    # Fallback to remote raw github if installed via curl | sh
    SCRIPT_SRC="$TARGET_DIR/anindo"
    printf "${C_BLUE}==>${C_RESET} Mengunduh anindo...\n"
    curl -sL https://raw.githubusercontent.com/Zirosaur/anindo/main/anindo -o "$SCRIPT_SRC"
else
    cp "$SCRIPT_SRC" "$TARGET_DIR/anindo"
fi

chmod +x "$TARGET_DIR/anindo"
ln -sf "$TARGET_DIR/anindo" "$TARGET_DIR/ani-cli-id"

# Check PATH
case ":$PATH:" in
    *:"$TARGET_DIR":*) ;;
    *)
        printf "${C_YELLOW}[INFO]${C_RESET} Tambahkan $TARGET_DIR ke PATH jika belum ada:\n"
        printf "  export PATH=\"\$HOME/.local/bin:\$PATH\"\n"
        ;;
esac

printf "${C_GREEN}${C_BOLD}✓ anindo berhasil dipasang di %s/anindo!${C_RESET}\n" "$TARGET_DIR"
printf "Jalankan dengan mengetik: ${C_CYAN}anindo${C_RESET} atau ${C_CYAN}ani-cli-id${C_RESET}\n"
