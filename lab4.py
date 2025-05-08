import numpy 
import matplotlib.pyplot as plt
def reader(filename):# Функция для чтения матрицы из файла
    with open(filename, 'r') as file:
        return [list(map(int, line.split())) for line in file]
k = int(input("Введите k: "))# Ввод параметров
n = int(input("Введите n: "))
A=reader('matrix2.txt') 
A=numpy.copy(A)
print("Матрица А:\n", A)
F = numpy.copy(A)# Создаем копию матрицы A для F
count_polozh, count_otric = 0, 0
if n % 2 == 0: # Определяем размер подматриц
    r = n // 2
else:
    r = (n - 1) // 2 + 1
for i in range(r, n):# Подсчет положительных и отрицательных элементов
    for j in range(r if n % 2 == 0 else r - 1):
        if F[i][j] > 0 and (j + 1) % 2 == 0:
            count_polozh += 1
        if F[i][j] < 0 and (j + 1) % 2 != 0:
            count_otric += 1
# Преобразование матрицы F по условию
if count_polozh > count_otric: # Симметричный обмен
    for i in range(r, n):
        x = n - 1
        for j in range(r if n % 2 == 0 else r - 1):
            F[i][j], F[i][x] = F[i][x], F[i][j]
            x -= 1
else: # Несимметричный обмен
    for i in range(r, n):
        for j in range(r if n % 2 == 0 else r - 1):
            F[i][j], F[i - r][j + r] = F[i - r][j + r], F[i][j]

print("Матрица F:\n", F)

try: # Вычисление необходимых матриц
    C = numpy.linalg.inv(A)
    G = numpy.tril(A)
except numpy.linalg.LinAlgError:
    print("Матрица A вырождена, невозможно вычислить обратную матрицу")
    exit()

if round(numpy.linalg.det(A)) > numpy.trace(F):# Вычисление результата по условию
    VIR = numpy.subtract(numpy.dot(A, A.T), k * numpy.dot(F, C))
    print("\nТранспонированная матрица A:\n", A.T)
    print("\nМатрица, обратная A:\n", C)
    print("\nМатрица A, умноженная на свою транспонированную версию:\n", numpy.dot(A, A.T))
    print("\nМатрица F, умноженная на матрицу, обратную A:\n", numpy.dot(F, C))
    print("\nМатрица k*F*invA:\n", k * numpy.dot(F, C))
    print("\nРезультат вычислений:\n", VIR)
else:
    VIR = k * (numpy.subtract(numpy.add(k * C, G), F.T))
    print("\nТранспонированная матрица F:\n", F.T)
    print("\nНижняя треугольная матрица G:\n", G)
    print("\nМатрица, обратная A:\n", C)
    print("\nМатрица k*invA:\n", k * C)
    print("\nМатрица k*invA+G:\n", numpy.add(k * C, G))
    print("\nМатрица k*invA+G-F.T:\n", numpy.subtract(numpy.add(k * C, G), F.T))
    print("\nРезультат вычислений:\n", VIR)

plt.figure(figsize=(15, 5))# Построение графиков
# 1. Тепловая карта матрицы F
plt.subplot(131)
plt.imshow(F, cmap='winter', interpolation='nearest')
plt.colorbar()
plt.title("Тепловая карта F")
# 2. График суммы по строкам
plt.subplot(132)
plt.plot(F.sum(axis=1), 'o-', color='cyan')
plt.title("Сумма по строкам")
plt.grid(True)
# 3. Столбчатая диаграмма суммы по столбцам
plt.subplot(133)
plt.bar(range(F.shape[1]), F.sum(axis=0), color='cyan', alpha=0.6)
plt.title("Сумма по столбцам")
plt.grid(True)
plt.tight_layout()
plt.show()