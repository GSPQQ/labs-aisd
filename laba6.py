import math
import timeit
import matplotlib.pyplot as plt

# Рекурсивная функция F(n)
def F_rec(n):
    if n < 3:
        return 3
    elif 3 < n <= 25:
        return F_rec(n - 1)
    else:
        sign = -1 if n % 2 == 0 else 1
        return sign * (5 * F_rec(n - 1) / math.factorial(2 * n) - 2 * (n - 2))

# Итерационная функция F(n)
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
            fact = 1
            for j in range(1, 2*i + 1):
                fact *= j
            f_current = sign * (5 * f_prev) / fact - 2 * (i - 2)
        f_prev = f_current
    
    return f_prev

def measure_time(func, n):
    return timeit.timeit(lambda: func(n), number=100)

def main():
    n = int(input("Введите натуральное число N: "))

    results = {
        'n': [],
        'F_rec': [],
        'F_iter': [],
        'time_rec': [],
        'time_iter': []
    }

    for i in range(1, n + 1):
        results['n'].append(i)

        # Рекурсивные вычисления
        start = timeit.default_timer()
        f_rec = F_rec(i)
        time_rec = (timeit.default_timer() - start) * 1000

        # Итерационные вычисления
        start = timeit.default_timer()
        f_iter = F_iter(i)
        time_iter = (timeit.default_timer() - start) * 1000

        results['F_rec'].append(f_rec)
        results['F_iter'].append(f_iter)
        results['time_rec'].append(time_rec)
        results['time_iter'].append(time_iter)

    # Вывод результатов
    print("\nРезультаты вычислений:")
    print(f"{'n':<5}{'F рекурсивно':<20}{'F итерационно':<20}{'Время рекурсии (мс)':<20}{'Время итерации (мс)':<20}")
    for i in range(n):
        print(f"{results['n'][i]:<5}"
              f"{results['F_rec'][i]:<20.6f}"
              f"{results['F_iter'][i]:<20.6f}"
              f"{results['time_rec'][i]:<20.4f}"
              f"{results['time_iter'][i]:<20.4f}")

    # Визуализация

    plt.plot(results['n'], results['time_rec'], 'r-', label='Рекурсия')
    plt.plot(results['n'], results['time_iter'], 'b-', label='Итерация')
    plt.title('время сравнения итерации и рекурсии')
    plt.xlabel('n')
    plt.ylabel('время')
    plt.legend()
    plt.grid(True)
    plt.show()

    

if __name__ == "__main__":
    main()