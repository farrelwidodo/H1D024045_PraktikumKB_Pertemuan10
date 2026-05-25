import random

# Fungsi untuk Roulette Wheel Selection
def roulette_wheel_selection(populasi, fitness_populasi):
    total_fitness = sum(fitness_populasi)
    if total_fitness == 0:
        idx = random.randrange(len(populasi))
        return populasi[idx], idx  # Mengembalikan individu dan indeksnya

    probabilitas = [fitness / total_fitness for fitness in fitness_populasi]
    kumulatif_prob = []
    kumulatif = 0
    for p in probabilitas:
        kumulatif += p
        kumulatif_prob.append(kumulatif)

    r = random.random()
    for i, kum_prob in enumerate(kumulatif_prob):
        if r <= kum_prob:
            return populasi[i], i  # Mengembalikan individu dan indeksnya
    return populasi[-1], len(populasi)-1  # Fallback

# Fungsi untuk Tournament Selection
def tournament_selection(populasi, fitness_populasi, k=3):
    if len(populasi) < k:
        k = len(populasi)
    peserta_indices = random.sample(range(len(populasi)), k)
    peserta = [(populasi[i], fitness_populasi[i], i) for i in peserta_indices]
    peserta.sort(key=lambda x: x[1], reverse=True)
    return peserta[0][0], peserta[0][2]  # Mengembalikan individu dan indeksnya

if __name__ == "__main__":
    # Definisikan populasi awal dan fitness_populasi
    populasi_awal = ['individu1', 'individu2', 'individu3', 'individu4']
    fitness_populasi = [10, 20, 30, 40]

    # Membuat salinan populasi dan fitness untuk dimodifikasi
    available_populasi = populasi_awal.copy()
    available_fitness = fitness_populasi.copy()

    # Memilih Parent 1 menggunakan Roulette Wheel Selection
    parent1, idx1 = roulette_wheel_selection(available_populasi, available_fitness)
    del available_populasi[idx1]
    del available_fitness[idx1]

    # Memilih Parent 2 menggunakan Tournament Selection
    parent2, idx2 = tournament_selection(available_populasi, available_fitness)
    del available_populasi[idx2]
    del available_fitness[idx2]

    print("\nParent Terpilih:")
    print(f"Parent 1: {parent1}")
    print(f"Parent 2: {parent2}")
