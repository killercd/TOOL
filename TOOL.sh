#!/bin/bash


GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

BIN_LIST=("sqlite3" "curl" "wget" "sqlmap" "nmap" "nikto" "sqlitebrowser")

install_bin(){
    bin_name=$1
    echo -e "$BLUE[*] Installing $bin_name$NC"
    
    if [[ -x "$(command -v apt-get)" ]]; then
        sudo apt-get update
        sudo apt-get install -y $bin_name
    elif [[ -x "$(command -v yum)" ]]; then
        sudo yum install -y $bin_name
    elif [[ -x "$(command -v dnf)" ]]; then
        sudo dnf install -y $bin_name
    elif [[ -x "$(command -v pacman)" ]]; then
        sudo pacman -Sy $bin_name
    else
        echo "[!] Unable to locate package manager"
        exit 1
    fi
    echo -e "$GREEN $bin_name [OK]$NC"
}

install_dependencies(){
    echo "[*] Checking dependencies..."
    for bin_name in "${BIN_LIST[@]}"; do
        echo "[*] Checking $bin_name"
        if ! command -v $bin_name >/dev/null 2>&1; then
            install_bin $bin_name
        else
            echo -e "$BLUE $bin_name is already installed$NC"
        fi
    done

}


install_dependencies

