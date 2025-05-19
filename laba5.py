import timeit
n = 10000
d = 2
def generate_numbers_with_limit(n, d):
    result = []
    for i in range(1, n + 1):
        if len(str(i)) <= d and is_odd_start_end(i):
            result.append(i)
    return result

def is_odd_start_end(num):
    num_str = str(num)
    return num_str[0] in '13579' and num_str[-1] in '13579'

numbers = generate_numbers_with_limit(n, d)
print(numbers)
def generate_numbers_functional_with_limit(n, d):
    return list(filter(lambda x: len(str(x)) <= d and str(x)[0] in '13579' and str(x)[-1] in '13579', range(1, n + 1)))
numbers = generate_numbers_functional_with_limit(n, d)
print(numbers)

# Алгоритмический подход с ограничением
algorithmic_time_with_limit = timeit.timeit(lambda: generate_numbers_with_limit(n, d), number=100)
print(f"Алгоритмический подход с ограничением: {algorithmic_time_with_limit} секунд")

# Функциональный подход с ограничением
functional_time_with_limit = timeit.timeit(lambda: generate_numbers_functional_with_limit(n, d), number=100)
print(f"Функциональный подход с ограничением: {functional_time_with_limit} секунд")