# Вариант11.Формируется матрица F следующим образом: скопировать в нее А и если в С сумма 
# чисел  в нечетных столбцах больше, чем произведение чисел в четных строках, то поменять местами В и С симметрично, иначе Е и В поменять местами несимметрично
# При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,то вычисляется выражение:A-1*AT – K * F-1, 
# полученная из А. Выводятся по мере формирования А, F и все матричные операции последовательно.
#иначе вычисляется выражение (AТ +G-1-F-1)*K, где G-нижняя треугольная матрица, 
import numpy as np
import matplotlib.pyplot as plt
def reader(filename):  
    with open(filename, 'r') as file:
        return [list(map(int, line.split())) for line in file]
k = int(input("Введите k: "))
n = int(input("Введите n: "))
A = np.array(reader('matrix2.txt'))[:n, :n]  
print("Матрица A:\n", A)
F = np.copy(A)  
half = n // 2
E = F[half:, :half] if n % 2 == 0 else F[half + 1:, :half + 1]
count_polozh = np.sum((E > 0) & (np.arange(E.shape[1]) % 2 == 1))  
count_otric = np.sum((E < 0) & (np.arange(E.shape[1]) % 2 == 0))   
if count_polozh > count_otric:
    if n % 2 == 0:
        B = F[half:, half:].copy()
        C = F[:half, half:].copy()
        F[:half, half:] = np.fliplr(B)
        F[half:, half:] = np.fliplr(C)
    else:
        B = F[half + 1:, half + 1:].copy()
        C = F[:half, half + 1:].copy()
        F[:half, half + 1:] = np.fliplr(B)
        F[half + 1:, half + 1:] = np.fliplr(C)
else:
    if n % 2 == 0:
        E = F[half:, :half].copy()
        B = F[half:, half:].copy()
        F[half:, :half] = B
        F[half:, half:] = E
    else:
        E = F[half + 1:, :half + 1].copy()
        B = F[half + 1:, half + 1:].copy()
        F[half + 1:, :half + 1] = B
        F[half + 1:, half + 1:] = E
print("Матрица F:\n", F)
try:
    A_inv = np.linalg.inv(A)
    G = np.tril(A)
except np.linalg.LinAlgError:
    print("Матрица A вырождена, невозможно вычислить обратную матрицу")
    exit()
# Вычисление результата по условию
if round(np.linalg.det(A)) > np.trace(F):
    VIR = np.subtract(np.dot(A, A.T), k * np.dot(F, A_inv))
    print("\nТранспонированная матрица A:\n", A.T)
    print("\nМатрица, обратная A:\n", A_inv)
    print("\nМатрица A, умноженная на свою транспонированную версию:\n", np.dot(A, A.T))
    print("\nМатрица F, умноженная на матрицу, обратную A:\n", np.dot(F, A_inv))
    print("\nМатрица k*F*invA:\n", k * np.dot(F, A_inv))
    print("\nРезультат вычислений:\n", VIR)
else:
    VIR = k * (np.subtract(np.add(A_inv, G), F.T))
    print("\nТранспонированная матрица F:\n", F.T)
    print("\nНижняя треугольная матрица G:\n", G)
    print("\nМатрица, обратная A:\n", A_inv)
    print("\nМатрица k*invA:\n", k * A_inv)
    print("\nМатрица k*invA+G:\n", np.add(k *A_inv, G))
    print("\nМатрица k*invA+G-F.T:\n", np.subtract(np.add(k * A_inv, G), F.T))
    print("\nРезультат вычислений:\n", VIR)
# Визуализация
plt.figure(figsize=(15, 5))
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
