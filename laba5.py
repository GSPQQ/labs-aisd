import itertools
import timeit
from math import inf

MAX_ELEMENTS = 8  # Максимальное разрешённое K*T

def generate_arrays_recursive(K, T):
    """Рекурсивная генерация всех возможных массивов K×T из чисел 0, 1, 2"""
    if K * T > MAX_ELEMENTS:
        raise ValueError(f"Превышен максимальный размер массива {MAX_ELEMENTS} элементов")
    
    total_elements = K * T
    arrays = []
    
    def backtrack(current):
        if len(current) == total_elements:
            arrays.append([current[i*T:(i+1)*T] for i in range(K)])
            return
        for num in [0, 1, 2]:
            backtrack(current + [num])
    
    backtrack([])
    return arrays

def generate_arrays_itertools(K, T):
    """Генерация массивов K×T из чисел 0, 1, 2 с помощью itertools.product"""
    if K * T > MAX_ELEMENTS:
        raise ValueError(f"Превышен максимальный размер массива {MAX_ELEMENTS} элементов")
    
    total_elements = K * T
    products = itertools.product([0, 1, 2], repeat=total_elements)
    return [[list(product[i*T:(i+1)*T]) for i in range(K)] for product in products]

def find_optimal_array(K, T, criterion):
    """
    Находит оптимальный массив по заданному критерию.
    criterion: функция, принимающая массив и возвращающая числовое значение
    Возвращает оптимальный массив и его значение критерия
    """
    if K * T > MAX_ELEMENTS:
        raise ValueError(f"Превышен максимальный размер массива {MAX_ELEMENTS} элементов")
    
    arrays = generate_arrays_itertools(K, T)
    optimal_array = None
    optimal_value = inf
    
    for array in arrays:
        current_value = criterion(array)
        if current_value < optimal_value:
            optimal_value = current_value
            optimal_array = array
    
    return optimal_array, optimal_value

def compare_methods(K, T, number=10):
    """Сравнение времени работы методов с использованием timeit"""
    try:
        print(f"\n=== Сравнение для массива {K}×{T} (всего {3**(K*T)} вариантов) ===")
        
        # Определяем критерий оптимальности (пример: минимизация суммы элементов)
        def sum_criterion(array):
            return sum(sum(row) for row in array)
        
        # Находим оптимальный массив
        start_time = timeit.default_timer()
        optimal_array, optimal_value = find_optimal_array(K, T, sum_criterion)
        elapsed_time = timeit.default_timer() - start_time
        
        print(f"\nОптимальный массив (по критерию суммы элементов):")
        for row in optimal_array:
            print(row)
        print(f"Сумма элементов: {optimal_value}")
        print(f"Время поиска: {elapsed_time:.4f} секунд")
        
        # Выводим примеры массивов (только для небольших размеров)
        if K * T <= 6:  
            sample = generate_arrays_itertools(K, T)[:3]
            print("\nПримеры первых 3 массивов:")
            for i, arr in enumerate(sample, 1):
                print(f"{i}.")
                for row in arr:
                    print(" ", row)
    
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    # Тестируем на разных размерах
    test_cases = [(2, 2), (2, 3), (3, 2), (3, 3), (2, 5)]
    
    for K, T in test_cases:
        compare_methods(K, T, number=10)
