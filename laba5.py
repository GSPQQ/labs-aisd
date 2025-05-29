import itertools


def generate_matrices_itertools(K, T):
    """Генерация матриц с использованием itertools.permutations"""
    if T > 3:
        raise ValueError("T не может быть больше 3 (не хватит уникальных чисел 0,1,2)")
    
    # Все возможные строки (перестановки 0,1,2 длиной T)
    possible_rows = list(itertools.permutations([0, 1, 2], T))
    
    # Генерируем все комбинации строк
    matrix_combinations = itertools.product(possible_rows, repeat=K)
    
    # Преобразуем в список списков
    return [[list(row) for row in matrix] for matrix in matrix_combinations]

def find_optimal_matrix(matrices):
    """Находит матрицу с максимальной суммой элементов"""
    if not matrices:
        return None, -1
    
    max_sum = -1
    optimal_matrix = None
    
    for matrix in matrices:
        current_sum = sum(sum(row) for row in matrix)
        if current_sum > max_sum:
            max_sum = current_sum
            optimal_matrix = matrix
    
    return optimal_matrix, max_sum

def main():
    K = int(input("Введите K (количество строк): "))
    T = int(input("Введите T (количество столбцов, не больше 3): "))
    
    try:
        itertools_matrices = generate_matrices_itertools(K, T)
        optimal_itertools, sum_itertools = find_optimal_matrix(itertools_matrices)
        print(f"Найдено матриц: {len(itertools_matrices)}")
        print(f"Оптимальная матрица (сумма = {sum_itertools}):")
        for row in optimal_itertools:
            print(row)
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
