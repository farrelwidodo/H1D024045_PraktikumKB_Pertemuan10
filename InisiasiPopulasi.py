import random

# Fungsi untuk inisialisasi populasi
def inisialisasi_populasi(jumlah_populasi, jumlah_gen):
    populasi = []
    for i in range(jumlah_populasi):
        # Membuat kromosom dengan gen biner secara acak
        kromosom = [random.randint(0, 1) for _ in range(jumlah_gen)]
        populasi.append(kromosom)
    return populasi

# Contoh penggunaan
if __name__ == "__main__":
    jumlah_populasi = 10  # Jumlah individu dalam populasi
    jumlah_gen = 5        # Jumlah barang (gen) dalam kromosom

    populasi_awal = inisialisasi_populasi(jumlah_populasi, jumlah_gen)

    # Menampilkan populasi awal
    print("Populasi Awal:")
    for idx, individu in enumerate(populasi_awal):
        print(f"Individu {idx+1}: {individu}")
