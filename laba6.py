"""
Лабораторная работа №6
Сравнительное исследование рекурсивного и итерационного вычисления функции F(n)
F(n<2) = -2; F(n) = (-1)^n*(F(n-1) // (n-1)!)
"""

import math
import timeit
import matplotlib.pyplot as plt

# Рекурсивная реализация
def F_recursive(n):
    if n < 2:
        return -2
    sign = -1 if n % 2 == 0 else 1
    return sign * (F_recursive(n-1) // math.factorial(n-1))

# Итерационная реализация с оптимизацией
def F_iterative(n):
    if n < 2:
        return -2  
    F_prev = -2  # F(1)
    fact = 1     # 0! = 1
    sign = -1    # Начинаем с n=2
    for i in range(2, n+1):
        fact *= (i-1)
        F_current = sign * (F_prev // fact)
        F_prev = F_current
        sign *= -1
    return F_prev
def measure_performance():
    max_n = 20
    n_values = list(range(1, max_n + 1))
    rec_times = []
    iter_times = []
    rec_values = []
    iter_values = []
    
    for n in n_values:
        # Рекурсивный метод
        try:
            rec_time = timeit.timeit(lambda: F_recursive(n), number=100)
            rec_val = F_recursive(n)
        except RecursionError:
            rec_time = float('inf')
            rec_val = None
        
        # Итерационный метод
        iter_time = timeit.timeit(lambda: F_iterative(n), number=100)
        iter_val = F_iterative(n)
        
        rec_times.append(rec_time * 1000)
        iter_times.append(iter_time * 1000)
        rec_values.append(rec_val)
        iter_values.append(iter_val)
    
    return n_values, rec_times, iter_times, rec_values, iter_values

def print_results_table(n_values, rec_values, iter_values, rec_times, iter_times):
    print("\nСравнительная таблица результатов:")
    print("+" + "-"*6 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*22 + "+" + "-"*22 + "+")
    print("| {:^4} | {:^14} | {:^14} | {:^20} | {:^20} |".format(
        "n", "F рекурсивно", "F итерационно", "Время рекурсии (мс)", "Время итерации (мс)"))
    print("+" + "-"*6 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*22 + "+" + "-"*22 + "+")
    
    for i, n in enumerate(n_values):
        rec_val = rec_values[i] if rec_values[i] is not None else "Ошибка"
        rec_time = f"{rec_times[i]:.4f}" if rec_times[i] != float('inf') else "Ошибка"
        
        print("| {:^4} | {:^14} | {:^14} | {:^20} | {:^20} |".format(
            n, 
            str(rec_val),
            str(iter_values[i]),
            rec_time,
            f"{iter_times[i]:.4f}"
        ))
    
    print("+" + "-"*6 + "+" + "-"*16 + "+" + "-"*16 + "+" + "-"*22 + "+" + "-"*22 + "+")

def plot_results(n_values, rec_times, iter_times, rec_values, iter_values):
    plt.figure(figsize=(12, 6))
    
    # График времени выполнения
    plt.subplot(1, 2, 1)
    plt.plot(n_values, rec_times, 'r-', label='Рекурсия')
    plt.plot(n_values, iter_times, 'b-', label='Итерация')
    plt.xlabel('n')
    plt.ylabel('Время выполнения (мс)')
    plt.title('Сравнение времени вычисления')
    plt.legend()
    plt.grid()
    
    # График значений функции
    plt.subplot(1, 2, 2)
    valid_n = [n for i, n in enumerate(n_values) if rec_values[i] is not None]
    valid_rec = [v for v in rec_values if v is not None]
    plt.plot(valid_n, valid_rec, 'r-', label='F рекурсивно')
    plt.plot(n_values, iter_values, 'b--', label='F итерационно')
    plt.xlabel('n')
    plt.ylabel('Значение F(n)')
    plt.title('Сравнение значений функции')
    plt.legend()
    plt.grid()
    
    plt.tight_layout()
    plt.show()

def find_recursion_limit():
    n = 1
    while True:
        try:
            F_recursive(n)
            n += 1
        except RecursionError:
            return n - 1

def main():
    print("Лабораторная работа №6")
    print("Сравнение рекурсивного и итерационного вычисления функции F(n)")
    
    # Измерение производительности
    n_values, rec_times, iter_times, rec_values, iter_values = measure_performance()
    
    # Вывод таблицы результатов
    print_results_table(n_values, rec_values, iter_values, rec_times, iter_times)
    
    # Построение графиков
    plot_results(n_values, rec_times, iter_times, rec_values, iter_values)
    
    # Определение предела рекурсии
    limit = find_recursion_limit()
    print(f"\nПредел рекурсии: n = {limit}")
    
    # Вывод рекомендаций
    print("\nРекомендации:")
    print("1. Для n < 15 можно использовать любой метод")
    print("2. Для n >= 15 предпочтительнее итерационный метод")
    print(f"3. Рекурсивный метод перестает работать при n > {limit}")

if __name__ == "__main__":
    main()
