import itertools

def generate_matrices_recursive(K, T):
    """Рекурсивный метод с отсечением невалидных строк"""
    matrices = []
    
    def is_valid_row(row):
        return len(row) == len(set(row))  # Проверка на уникальность
    
    def backtrack(current_matrix, position):
        if position == K * T:
            # Формируем матрицу
            matrix = []
            for i in range(K):
                row = current_matrix[i*T : (i+1)*T]
                matrix.append(row)
            matrices.append(matrix)
            return
        
        row_idx = position // T
        col_idx = position % T
        
        for num in [0, 1, 2]:
            # Проверяем, что число не повторяется в текущей строке
            if num in current_matrix[row_idx*T : row_idx*T + col_idx]:
                continue
            current_matrix.append(num)
            backtrack(current_matrix, position + 1)
            current_matrix.pop()
    
    backtrack([], 0)
    return matrices

def generate_matrices_itertools(K, T):
    """Метод с itertools.permutations (быстрее, но требует T <= 3)"""
    if T > 3:
        raise ValueError("T не может быть больше 3 (не хватит уникальных чисел 0, 1, 2)")
    
    # Все возможные строки (перестановки 0, 1, 2 длиной T)
    possible_rows = list(itertools.permutations([0, 1, 2], T))
    
    # Генерируем все комбинации строк
    matrices = itertools.product(possible_rows, repeat=K)
    
    # Преобразуем в нужный формат
    return [ [list(row) for row in matrix] for matrix in matrices ]

def find_optimal_matrix(matrices):
    """Находит матрицу с максимальной суммой элементов"""
    max_sum = -1
    optimal_matrix = None
    
    for matrix in matrices:
        current_sum = sum(sum(row) for row in matrix)
        if current_sum > max_sum:
            max_sum = current_sum
            optimal_matrix = matrix
    
    return optimal_matrix, max_sum

def main():
    K = int(input())
    T = int(input("не больше 3"))
    
    print("=== Рекурсивный метод ===")
    matrices_recursive = generate_matrices_recursive(K, T)
    optimal_recursive, sum_recursive = find_optimal_matrix(matrices_recursive)
    print(f"Всего матриц: {len(matrices_recursive)}")
    print(f"Оптимальная матрица (сумма = {sum_recursive}):")
    for row in optimal_recursive:
        print(row)
    
    print("\n=== Метод с itertools ===")
    try:
        matrices_itertools = generate_matrices_itertools(K, T)
        optimal_itertools, sum_itertools = find_optimal_matrix(matrices_itertools)
        print(f"Всего матриц: {len(list(matrices_itertools))}")
        print(f"Оптимальная матрица (сумма = {sum_itertools}):")
        for row in optimal_itertools:
            print(row)
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
