import random
import matplotlib.pyplot as plt

# ============================================================
# NIM    : H1D024045
# Nama   : Farrel Wildan Widodo
# Metode Seleksi  : Roulette Wheel Selection (RWS) -> digit 4
# Metode Crossover: Uniform Crossover             -> digit 5
# Metode Mutasi   : Swap Mutation                 -> 4+5=9 -> Swap
# ============================================================

# --- Data Barang Tugas Pertemuan 10 ---
# Barang  Keuntungan  Ukuran
# Barang1     10        5
# Barang2     40        4
# Barang3     30        6
# Barang4     50        3
# Barang5     35        7
# Ukuran Maksimal Gudang: 15

barang = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7),
]

KAPASITAS_GUDANG = 15

# ============================================================
# FUNGSI INISIALISASI POPULASI
# ============================================================
def inisialisasi_populasi(jumlah_populasi, jumlah_gen):
    populasi = []
    for _ in range(jumlah_populasi):
        kromosom = [random.randint(0, 1) for _ in range(jumlah_gen)]
        populasi.append(kromosom)
    return populasi

# ============================================================
# FUNGSI EVALUASI FITNESS
# ============================================================
def hitung_fitness(kromosom, barang, kapasitas):
    total_keuntungan = 0
    total_ukuran = 0
    for i in range(len(kromosom)):
        if kromosom[i] == 1:
            total_keuntungan += barang[i][1]
            total_ukuran += barang[i][2]
    if total_ukuran > kapasitas:
        return 0  # Penalti jika melebihi kapasitas
    return total_keuntungan

# ============================================================
# FUNGSI SELEKSI - Roulette Wheel Selection (RWS)
# ============================================================
def roulette_wheel_selection(populasi, fitness_populasi):
    total_fitness = sum(fitness_populasi)
    if total_fitness == 0:
        idx = random.randrange(len(populasi))
        return populasi[idx], idx

    probabilitas = [f / total_fitness for f in fitness_populasi]
    kumulatif_prob = []
    kumulatif = 0
    for p in probabilitas:
        kumulatif += p
        kumulatif_prob.append(kumulatif)

    r = random.random()
    for i, kum_prob in enumerate(kumulatif_prob):
        if r <= kum_prob:
            return populasi[i], i
    return populasi[-1], len(populasi)-1

# ============================================================
# FUNGSI CROSSOVER - Uniform Crossover
# ============================================================
def uniform_crossover(parent1, parent2):
    mask = [random.randint(0, 1) for _ in range(len(parent1))]
    anak1, anak2 = [], []
    for i in range(len(parent1)):
        if mask[i] == 0:
            anak1.append(parent1[i])
            anak2.append(parent2[i])
        else:
            anak1.append(parent2[i])
            anak2.append(parent1[i])
    return anak1, anak2

# ============================================================
# FUNGSI MUTASI - Swap Mutation
# ============================================================
def swap_mutation(kromosom):
    kromosom = list(kromosom)
    posisi1, posisi2 = random.sample(range(len(kromosom)), 2)
    kromosom[posisi1], kromosom[posisi2] = kromosom[posisi2], kromosom[posisi1]
    return kromosom

# ============================================================
# FUNGSI UTAMA - Algoritma Genetika
# ============================================================
def run_ga(jumlah_generasi=50, jumlah_populasi=20,
           prob_crossover=0.8, prob_mutasi=0.1):

    jumlah_gen = len(barang)
    populasi = inisialisasi_populasi(jumlah_populasi, jumlah_gen)

    best_fitness_list = []
    worst_fitness_list = []
    avg_fitness_list = []
    all_fitness = []

    best_individu = None
    best_fitness_overall = 0

    for generasi in range(jumlah_generasi):
        fitness_populasi = [hitung_fitness(ind, barang, KAPASITAS_GUDANG)
                            for ind in populasi]

        best_fitness = max(fitness_populasi)
        worst_fitness = min(fitness_populasi)
        avg_fitness = sum(fitness_populasi) / len(fitness_populasi)

        best_fitness_list.append(best_fitness)
        worst_fitness_list.append(worst_fitness)
        avg_fitness_list.append(avg_fitness)
        all_fitness.append(fitness_populasi.copy())

        if best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            best_individu = populasi[fitness_populasi.index(best_fitness)][:]

        new_populasi = []
        used_indices = []

        while len(new_populasi) < jumlah_populasi:
            # Seleksi Parent 1 - RWS
            parent1, idx1 = roulette_wheel_selection(populasi, fitness_populasi)
            used_indices.append(idx1)

            # Seleksi Parent 2 - RWS (berbeda dari parent1)
            available_indices = [i for i in range(len(populasi)) if i not in used_indices]
            if not available_indices:
                used_indices = [idx1]
                available_indices = [i for i in range(len(populasi)) if i != idx1]

            parent2, idx2_rel = roulette_wheel_selection(
                [populasi[i] for i in available_indices],
                [fitness_populasi[i] for i in available_indices]
            )
            used_indices.append(available_indices[idx2_rel])

            # Crossover - Uniform
            if random.random() < prob_crossover:
                anak1, anak2 = uniform_crossover(parent1, parent2)
            else:
                anak1, anak2 = parent1[:], parent2[:]

            # Mutasi - Swap
            if random.random() < prob_mutasi:
                anak1 = swap_mutation(anak1)
            if random.random() < prob_mutasi:
                anak2 = swap_mutation(anak2)

            new_populasi.extend([anak1, anak2])

        populasi = new_populasi[:jumlah_populasi]

    # ---- GRAFIK ----
    plt.figure(figsize=(12, 7))
    for i in range(jumlah_generasi):
        x = [i+1] * len(all_fitness[i])
        y = all_fitness[i]
        plt.scatter(x, y, color='gray', alpha=0.1)

    plt.plot(range(1, jumlah_generasi+1), best_fitness_list,
             color='blue', label='Fitness Tertinggi')
    plt.plot(range(1, jumlah_generasi+1), worst_fitness_list,
             color='yellow', label='Fitness Terendah')
    plt.plot(range(1, jumlah_generasi+1), avg_fitness_list,
             color='red', label='Fitness Rata-rata')

    plt.title('Perkembangan Nilai Fitness - Pertemuan 10\n'
              'H1D024045 | Farrel Wildan Widodo | '
              'Seleksi: RWS | Crossover: Uniform | Mutasi: Swap')
    plt.xlabel('Generasi')
    plt.ylabel('Nilai Fitness (Keuntungan)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # ---- HASIL AKHIR ----
    selected_items = [(barang[i][0], barang[i][1], barang[i][2])
                      for i in range(len(best_individu)) if best_individu[i] == 1]
    selected_value = hitung_fitness(best_individu, barang, KAPASITAS_GUDANG)
    selected_size  = sum(barang[i][2] for i in range(len(best_individu)) if best_individu[i] == 1)

    print(f"\n{'='*55}")
    print(f"  HASIL ALGORITMA GENETIKA - KNAPSACK PROBLEM")
    print(f"{'='*55}")
    print(f"  NIM    : H1D024045")
    print(f"  Nama   : Farrel Wildan Widodo")
    print(f"  Seleksi  : Roulette Wheel Selection (RWS)")
    print(f"  Crossover: Uniform Crossover")
    print(f"  Mutasi   : Swap Mutation")
    print(f"{'='*55}")
    print(f"  Ukuran Maksimal Gudang : {KAPASITAS_GUDANG}")
    print(f"  Keuntungan Maksimal    : {selected_value}")
    print(f"  Total Ukuran Terpakai  : {selected_size}")
    print(f"{'='*55}")
    print(f"  Barang yang Dibeli:")
    print(f"  {'Barang':<12} {'Keuntungan':>12} {'Ukuran':>8}")
    print(f"  {'-'*34}")
    for nama, keuntungan, ukuran in selected_items:
        print(f"  {nama:<12} {keuntungan:>12} {ukuran:>8}")
    print(f"  {'-'*34}")
    print(f"  {'TOTAL':<12} {selected_value:>12} {selected_size:>8}")
    print(f"{'='*55}\n")

# Jalankan GA
run_ga(
    jumlah_generasi=50,
    jumlah_populasi=20,
    prob_crossover=0.8,
    prob_mutasi=0.1
)
