import math
import timeit
import matplotlib.pyplot as plt

def F_rec(n):
    if n < 3:
        return 3
    elif 3 < n <= 25:
        return F_rec(n - 1)
    else:
        sign = -1 if n % 2 == 0 else 1
        return sign * (5 * F_rec(n - 1) / math.factorial(2 * n) - 2 * (n - 2))

def F_iter(n):
    if n < 3:
        return 3
    
    f_prev = 3
    current_fact = 1  
    
    for i in range(3, n + 1):
        if 3 < i <= 25:
            f_current = f_prev
        else:
            sign = -1 if i % 2 == 0 else 1
            current_fact = math.factorial(2 * i)
            f_current = sign * (5 * f_prev) / current_fact - 2 * (i - 2)
        f_prev = f_current
    
    return f_prev

def main():
    n = int(input("Введите N: "))
    
    results = {
        'n': list(range(1, n + 1)),
        'F_rec': [],
        'F_iter': [],
        'time_rec': [],
        'time_iter': []
    }

    for i in results['n']:
        # Замер времени для рекурсии
        start = timeit.default_timer()
        results['F_rec'].append(F_rec(i))
        results['time_rec'].append((timeit.default_timer() - start) * 1000)
        
        # Замер времени для итерации
        start = timeit.default_timer()
        results['F_iter'].append(F_iter(i))
        results['time_iter'].append((timeit.default_timer() - start) * 1000)

    # Вывод таблицы
    print("\nРезультаты:")
    print(f"{'n':<5}{'F_rec':<15}{'F_iter':<15}{'t_rec(мс)':<10}{'t_iter(мс)':<10}")
    for i in range(n):
        print(f"{results['n'][i]:<5}"
              f"{results['F_rec'][i]:<15.6f}"
              f"{results['F_iter'][i]:<15.6f}"
              f"{results['time_rec'][i]:<10.4f}"
              f"{results['time_iter'][i]:<10.4f}")

    # График
    plt.figure(figsize=(10, 5))
    plt.plot(results['n'], results['time_rec'], 'r-', label='Рекурсия')
    plt.plot(results['n'], results['time_iter'], 'b-', label='Итерация')
    plt.title('Сравнение времени выполнения')
    plt.xlabel('n')
    plt.ylabel('Время (мс)')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
