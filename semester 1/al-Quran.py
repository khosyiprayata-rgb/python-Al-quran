"""
Program Al-Qur'an API - Projek Akhir Semester
Mengambil data dari eQuran.id API dan menampilkan informasi surat serta ayat
"""

import requests
import json
from typing import Optional

# ==================== FUNGSI UTILITAS ====================

def tampilkan_header():
    """Menampilkan header program"""
    print("\n" + "="*60)
    print("        PROGRAM INFORMASI AL-QUR'AN")
    print("           Data dari eQuran.id API")
    print("="*60 + "\n")


def ambil_semua_surat() -> Optional[list]:
    """
    Mengambil data semua surat dari API
    Returns: List berisi data surat atau None jika gagal
    """
    url = "https://equran.id/api/v2/surat"
    
    try:
        print("📡 Mengambil data dari API...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error jika status code bukan 200
        
        data = response.json()
        return data.get('data', [])
    
    except requests.exceptions.Timeout:
        print("❌ Error: Koneksi timeout. Cek koneksi internet Anda.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil data: {e}")
        return None


def ambil_detail_surat(nomor_surat: int) -> Optional[dict]:
    """
    Mengambil detail surat beserta ayat-ayatnya
    Args:
        nomor_surat: Nomor surat (1-114)
    Returns: Dictionary berisi detail surat atau None jika gagal
    """
    url = f"https://equran.id/api/v2/surat/{nomor_surat}"
    
    try:
        print(f"📡 Mengambil detail surat nomor {nomor_surat}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data.get('data', {})
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil detail surat: {e}")
        return None


# ==================== FUNGSI TAMPILAN ====================

def tampilkan_semua_surat(data_surat: list):
    """
    Menampilkan daftar semua surat dalam bentuk tabel
    Args:
        data_surat: List berisi data surat
    """
    print("\n📚 DAFTAR SURAT AL-QUR'AN")
    print("-" * 90)
    print(f"{'No':<5} {'Nama Latin':<20} {'Nama Arab':<20} {'Arti':<25} {'Ayat':<5}")
    print("-" * 90)
    
    for surat in data_surat:
        nomor = surat.get('nomor', '-')
        nama_latin = surat.get('namaLatin', '-')
        nama_arab = surat.get('nama', '-')
        arti = surat.get('arti', '-')
        jumlah_ayat = surat.get('jumlahAyat', '-')
        
        # Batasi panjang string agar rapi
        nama_latin = nama_latin[:18] + '..' if len(nama_latin) > 20 else nama_latin
        arti = arti[:23] + '..' if len(arti) > 25 else arti
        
        print(f"{nomor:<5} {nama_latin:<20} {nama_arab:<20} {arti:<25} {jumlah_ayat:<5}")
    
    print("-" * 90)
    print(f"Total: {len(data_surat)} surat\n")


def tampilkan_detail_surat(detail: dict, jumlah_ayat: int = 5):
    """
    Menampilkan detail surat dan beberapa ayat
    Args:
        detail: Dictionary berisi detail surat
        jumlah_ayat: Jumlah ayat yang ingin ditampilkan
    """
    # Informasi surat
    print("\n" + "="*90)
    print(f"📖 Surat {detail.get('namaLatin', '')} ({detail.get('nama', '')})")
    print("="*90)
    print(f"Arti: {detail.get('arti', '')}")
    print(f"Tempat Turun: {detail.get('tempatTurun', '')}")
    print(f"Jumlah Ayat: {detail.get('jumlahAyat', '')}")
    print(f"Nomor Surat: {detail.get('nomor', '')}")
    print("-"*90)
    
    # Deskripsi singkat
    deskripsi = detail.get('deskripsi', '')
    if deskripsi:
        # Hapus HTML tags sederhana
        deskripsi_clean = deskripsi.replace('<p>', '').replace('</p>', '\n')
        deskripsi_clean = deskripsi_clean.replace('<i>', '').replace('</i>', '')
        deskripsi_clean = deskripsi_clean.replace('<br>', '\n')
        print(f"\nDeskripsi:\n{deskripsi_clean[:300]}...")
    
    # Tampilkan ayat-ayat
    ayat_list = detail.get('ayat', [])
    total_ayat = len(ayat_list)
    
    if ayat_list:
        print(f"\n📜 Menampilkan {min(jumlah_ayat, total_ayat)} ayat pertama:")
        print("-"*90)
        
        for i, ayat in enumerate(ayat_list[:jumlah_ayat], 1):
            nomor_ayat = ayat.get('nomorAyat', i)
            teks_arab = ayat.get('teksArab', '')
            teks_latin = ayat.get('teksLatin', '')
            terjemahan = ayat.get('teksIndonesia', '')
            
            print(f"\nAyat {nomor_ayat}:")
            print(f"  Arab    : {teks_arab}")
            print(f"  Latin   : {teks_latin}")
            print(f"  Arti    : {terjemahan}")
        
        print("-"*90)
        if total_ayat > jumlah_ayat:
            print(f"💡 Masih ada {total_ayat - jumlah_ayat} ayat lainnya di surat ini.")
    
    print()


def cari_surat(data_surat: list, kata_kunci: str) -> list:
    """
    Mencari surat berdasarkan nama (Latin atau arti)
    Args:
        data_surat: List berisi semua data surat
        kata_kunci: Kata kunci pencarian
    Returns: List surat yang cocok dengan pencarian
    """
    kata_kunci_lower = kata_kunci.lower()
    hasil = []
    
    for surat in data_surat:
        nama_latin = surat.get('namaLatin', '').lower()
        arti = surat.get('arti', '').lower()
        
        if kata_kunci_lower in nama_latin or kata_kunci_lower in arti:
            hasil.append(surat)
    
    return hasil


def statistik_surat(data_surat: list):
    """
    Menampilkan statistik dan perhitungan sederhana dari data surat
    Args:
        data_surat: List berisi data surat
    """
    total_surat = len(data_surat)
    total_ayat = sum(surat.get('jumlahAyat', 0) for surat in data_surat)
    rata_rata_ayat = total_ayat / total_surat if total_surat > 0 else 0
    
    # Surat terpanjang dan terpendek
    surat_terpanjang = max(data_surat, key=lambda x: x.get('jumlahAyat', 0))
    surat_terpendek = min(data_surat, key=lambda x: x.get('jumlahAyat', 0))
    
    # Kelompokkan berdasarkan tempat turun
    makkiyah = [s for s in data_surat if s.get('tempatTurun', '').lower() == 'mekah']
    madaniyah = [s for s in data_surat if s.get('tempatTurun', '').lower() == 'madinah']
    
    print("\n📊 STATISTIK AL-QUR'AN")
    print("="*60)
    print(f"Total Surat         : {total_surat}")
    print(f"Total Ayat          : {total_ayat}")
    print(f"Rata-rata Ayat/Surat: {rata_rata_ayat:.2f}")
    print("-"*60)
    print(f"Surat Terpanjang    : {surat_terpanjang.get('namaLatin')} ({surat_terpanjang.get('jumlahAyat')} ayat)")
    print(f"Surat Terpendek     : {surat_terpendek.get('namaLatin')} ({surat_terpendek.get('jumlahAyat')} ayat)")
    print("-"*60)
    print(f"Surat Makkiyah      : {len(makkiyah)} surat")
    print(f"Surat Madaniyah     : {len(madaniyah)} surat")
    print("="*60 + "\n")


# ==================== FUNGSI MENU ====================

def tampilkan_menu():
    """Menampilkan menu pilihan"""
    print("\n🔖 MENU PILIHAN:")
    print("1. Tampilkan semua surat")
    print("2. Cari surat berdasarkan nama")
    print("3. Lihat detail surat (dengan ayat-ayat)")
    print("4. Tampilkan statistik Al-Qur'an")
    print("5. Keluar")
    print("-" * 40)


def jalankan_program():
    """Fungsi utama untuk menjalankan program"""
    tampilkan_header()
    
    # Ambil data surat sekali di awal
    data_surat = ambil_semua_surat()
    
    if not data_surat:
        print("❌ Gagal mengambil data. Program dihentikan.")
        return
    
    print(f"✅ Berhasil memuat {len(data_surat)} surat\n")
    
    # Loop menu utama
    while True:
        tampilkan_menu()
        
        pilihan = input("Pilih menu (1-5): ").strip()
        
        if pilihan == "1":
            # Tampilkan semua surat
            tampilkan_semua_surat(data_surat)
        
        elif pilihan == "2":
            # Cari surat
            kata_kunci = input("\n🔍 Masukkan nama surat yang dicari: ").strip()
            hasil_cari = cari_surat(data_surat, kata_kunci)
            
            if hasil_cari:
                print(f"\n✅ Ditemukan {len(hasil_cari)} surat:")
                tampilkan_semua_surat(hasil_cari)
            else:
                print(f"\n❌ Tidak ditemukan surat dengan kata kunci '{kata_kunci}'")
        
        elif pilihan == "3":
            # Lihat detail surat
            try:
                nomor = int(input("\n📖 Masukkan nomor surat (1-114): ").strip())
                
                if 1 <= nomor <= 114:
                    detail = ambil_detail_surat(nomor)
                    if detail:
                        jumlah = int(input("Tampilkan berapa ayat? (default 5): ").strip() or "5")
                        tampilkan_detail_surat(detail, jumlah)
                else:
                    print("❌ Nomor surat harus antara 1-114")
            
            except ValueError:
                print("❌ Input harus berupa angka")
        
        elif pilihan == "4":
            # Statistik
            statistik_surat(data_surat)
        
        elif pilihan == "5":
            # Keluar
            print("\n✨ Terima kasih telah menggunakan program ini!")
            print("Jazakumullahu khairan 🤲\n")
            break
        
        else:
            print("\n❌ Pilihan tidak valid. Silakan pilih 1-5.")
        
        # Tanya apakah ingin melanjutkan
        if pilihan in ["1", "2", "3", "4"]:
            input("\nTekan Enter untuk kembali ke menu...")


# ==================== PROGRAM UTAMA ====================

if __name__ == "__main__":
    try:
        jalankan_program()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program dihentikan oleh user.")
        print("Jazakumullahu khairan 🤲\n")
    except Exception as e:
        print(f"\n❌ Terjadi error: {e}")
        print("Program dihentikan.\n")