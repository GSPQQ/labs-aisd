import random,copy
def reader(filename):
    with open(filename,'r') as file:
        return [list(map(int,line.split())) for line in file]
def print_matrix(m, title):
    print(f"\n{title}:")
    for row in m:
        print(" ".join(f"{x:4}" for x in row))
k,n=int(input('Введите число k ')),int(input('Введите число n '))
count_nechet,count_digit,x=0,0,n
A=reader('matrix.txt') 
print('Матрица А');[print(row) for row in A]
f=copy.deepcopy(A)
AT=[[0 for j in range(len(A))]for i in range(len(A[0]))]
for i in range(len(AT)):
    for j in range(len(AT)):
        AT[j][i]=A[i][j]
e=n-1
for i in range(n):
    for j in range(n):
        if i>j and j>e and (j+1)%2==0 and f[i][j]%2!=0:
            count_nechet+=1
    e-=1
e=n-1
for i in range(n):
    for j in range(n):
        if i<j and j>e and (i+1)%2==0:
            count_digit+=f[i][j]
    e-=1
e=n-1
if count_nechet>count_digit:
    for i in range(n):
        for j in range(n):
            if i>j and j>e:
                f[i][j], f[j][i] = f[j][i], f[i][j]
        e-=1
    print('Семетрично')
else:
    for i in range(n):
        for j in range(n):
            if i > j and j > e:
                f[i][j], f[x-1-j][i]=f[x-1-j][i], f[i][j]
        e-=1
print("Матрица F: "); [print(row) for row in f]
KA = [[k*x for x in row] for row in A]
KA_A = [[sum(KA[i][k]*A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
AT = [[A[j][i] for j in range(n)] for i in range(n)]
KAT = [[k*x for x in row] for row in AT]
res = [[KA_A[i][j]-KAT[i][j] for j in range(n)] for i in range(n)]
print_matrix(res, "(K*A)*A - K*Aᵀ")