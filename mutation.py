import random

# Swap Mutation
def swap_mutation(kromosom):
    # Pastikan kromosom adalah list
    kromosom = list(kromosom)
    # Pilih dua posisi untuk swap
    posisi1, posisi2 = random.sample(range(len(kromosom)), 2)
    # Melakukan swap
    kromosom[posisi1], kromosom[posisi2] = kromosom[posisi2], kromosom[posisi1]
    return kromosom

# Inversion Mutation
def inversion_mutation(kromosom):
    kromosom = list(kromosom)
    posisi1 = random.randint(0, len(kromosom) - 2)
    posisi2 = random.randint(posisi1 + 1, len(kromosom) - 1)
    kromosom[posisi1:posisi2] = list(reversed(kromosom[posisi1:posisi2]))
    return kromosom

# Uniform Mutation
def uniform_mutation(kromosom, mutation_rate=0.1):
    # Pastikan kromosom adalah list
    kromosom = list(kromosom)
    for i in range(len(kromosom)):
        if random.random() < mutation_rate:
            kromosom[i] = 1 - kromosom[i]  # Membalik nilai gen
    return kromosom

if __name__ == "__main__":
    anak1 = [0, 1, 1, 0, 1]  # Contoh kromosom

    mutasi_anak1 = swap_mutation(anak1.copy())       # Swap Mutation
    mutasi_anak2 = inversion_mutation(anak1.copy())  # Inversion Mutation
    mutasi_anak3 = uniform_mutation(anak1.copy())    # Uniform Mutation

    print("\nAnak Setelah Mutasi:")
    print(f"Anak 1 (Swap Mutation): {mutasi_anak1}")
    print(f"Anak 2 (Inversion Mutation): {mutasi_anak2}")
    print(f"Anak 3 (Uniform Mutation): {mutasi_anak3}")
