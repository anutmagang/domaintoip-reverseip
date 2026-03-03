import requests
import re
import socket
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- KONFIGURASI ENGINE ---

def clean_target(target):
    """Membersihkan URL/Path agar menyisakan Domain atau IP saja"""
    target = target.strip().replace('http://', '').replace('https://', '')
    # Menghapus path setelah '/' dan port setelah ':'
    return target.split('/')[0].split(':')[0]

def get_ip_from_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def engine_rapiddns(ip):
    try:
        url = f"https://rapiddns.io/s/{ip}?full=1#result"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=10)
        # Mengambil domain dari tabel HTML menggunakan regex
        domains = re.findall(r'<td>([^<>\s]+\.[a-zA-Z]{2,})</td>', res.text)
        return list(set(domains))
    except:
        return []

def engine_hackertarget(ip):
    try:
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        res = requests.get(url, timeout=10)
        if "API count exceeded" in res.text: 
            return []
        return [d for d in res.text.split('\n') if d]
    except:
        return []

def engine_sitedossier(ip):
    try:
        url = f"http://www.sitedossier.com/ip/{ip}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        return re.findall(r'<a href="/site/([^"]+)">', res.text)
    except:
        return []

# --- WORKER FUNCTION ---

def process_target(target):
    """Fungsi yang dijalankan oleh setiap thread"""
    target = clean_target(target)
    if not target: return []

    # Deteksi apakah target adalah format IP Address
    is_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target)
    
    if is_ip:
        # Jika input IP -> Jalankan Reverse IP (Cari Domain)
        d1 = engine_rapiddns(target)
        d2 = engine_hackertarget(target)
        d3 = engine_sitedossier(target)
        found = set(d1 + d2 + d3)
        if found:
            print(f"[+] IP {target} -> {len(found)} domain ditemukan")
            return list(found)
    else:
        # Jika input Domain -> Jalankan Domain to IP (Cari IP)
        ip_res = get_ip_from_domain(target)
        if ip_res:
            print(f"[+] Domain {target} -> IP: {ip_res}")
            return [ip_res]
    
    return []

# --- MAIN CONTROL ---

def main():
    print("\n" + "="*55)
    print("   ULTRA-RECON: DOMAIN & IP RESOLVER (FIXED VERSION)")
    print("="*55)
    
    file_input = input("[?] Masukkan nama file (contoh: list.txt): ")
    if not os.path.exists(file_input):
        print(f"[-] Error: File '{file_input}' tidak ditemukan di folder ini.")
        return

    try:
        thread_input = input("[?] Jumlah threads (Default 10, Rekomendasi 10-50): ")
        thread_count = int(thread_input) if thread_input.strip() else 10
    except ValueError:
        print("[!] Input salah, menggunakan default: 10 threads.")
        thread_count = 10
    
    # Membaca file target
    try:
        with open(file_input, 'r', encoding='utf-8', errors='ignore') as f:
            targets = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Gagal membaca file: {e}")
        return

    output_file = f"hasil_recon_{int(time.time())}.txt"
    final_data = set()

    print(f"\n[*] Memproses {len(targets)} target dengan {thread_count} threads...")
    print("[*] Harap tunggu sebentar...\n")

    # Eksekusi Multithreading (Paralel)
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        future_to_target = {executor.submit(process_target, t): t for t in targets}
        
        for future in as_completed(future_to_target):
            try:
                data = future.result()
                if data:
                    for item in data:
                        final_data.add(item)
            except Exception:
                pass

    # Menyimpan hasil ke file teks baru
    if final_data:
        with open(output_file, 'w') as out:
            for item in sorted(final_data):
                out.write(f"{item}\n")
        
        print("\n" + "="*55)
        print(f"[V] SELESAI!")
        print(f"[*] Total data unik didapat: {len(final_data)}")
        print(f"[*] Hasil disimpan di: {output_file}")
    else:
        print("\n[-] Tidak ada data yang berhasil didapatkan.")
    
    print("="*55 + "\n")

if __name__ == "__main__":
    main()
