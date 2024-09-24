#teste para criar filtros passa-baixa e passa-alta com máscaras de convolução
import numpy as np

altura = 2
largura = 3
bordas = 3 // 2

vetor = np.array([[1,1,1],
                  [1,1,1]])

kernel = np.array([[2,2,2],
                   [2,2,2],
                   [2,2,2]])

'''
    Tem que fazer um código pra adicionar essas bordas com valores 0, unindo tabela original com as bordas 0.
'''
auxVetor = np.array([[0,0,0,0,0],
                    [0,1,1,1,0],
                    [0,1,1,1,0],
                    [0,0,0,0,0]])

ini_array = np.array([[1, 2, 3], [45, 4, 7], [9, 6, 10]])
rowIni = 3
colIni = 3
# Array to be added as column
#ini_array = np.append(ini_array,0)

#código pra preencher a matriz auxiliar iniciado
zero = np.zeros(shape=(rowIni+(bordas*2),colIni+(bordas*2))).astype(int)
c = 0
for i in range(bordas,rowIni+bordas):
    #print(abs(rowIni-(bordas*2)))
    #print(colIni+bordas)
    zero[i][bordas:colIni+bordas] = ini_array[c]#1:4
    c += 1
#código pra preencher a matriz auxiliar finalizado

#ini_array = np.append(ini_array,0)
#zero[1:-1, 1:-1] = ini_array
#np.insert(zero, 1, ini_array, axis=1).reshape(4,4)
#for i in range(0,3):
 #   print(np.concatenate(([9],ini_array[i],[9])))

# Adding column to array using append() method
#arr = np.insert(ini_array, 0, column_to_be_added, axis=1)
print(f'valor de a \n{zero}')
exit()
tam = 3 #coluna limite (tam - 1) que o kernel vai estar
z = 0
x = 0
soma = 0
B = np.zeros(shape=(2, 3)).astype(int) #astype trnasforma os valores para int --np.int64--

print(f'borda {bordas}')
for i in range(0, altura):
    z = 0
    tam = 3
    #print(f'Estou no print do i z={z} e tam={tam}')
    for j in range(0, largura):
        x = i
        z = j
        #print(f'Estou no print do j z={z} e x={x}')
        soma = 0
        for p in range(0,3):
            z = j
            for r in range(0,3):
               # print(f'Estou no print do r M[{p}][{r}] * AUX[{x}][{z}]')
                #soma += 1
                print(f'kernel[{p}][{r}] = {kernel[p][r]} + auxVetor[{x}][{z}] = {auxVetor[x][z]}')
                soma += kernel[p][r] * auxVetor[x][z]
                z += 1
                #print(f'Estou no print do r z={z}')
           
            x += 1
            #print(f'Estou no print do p x={x}')
        print(f'soma = {soma}')
        tam += 1
        #print(f'Estou no print do j tam={tam}')
        if soma > 255: #normalização, pixels variam de 0-255
            soma = 255
        B[i][j] = soma #usar matriz original em vez de B
        #print(f'B[{i}{j}] = {soma}')

print(f'Matriz resultante')
print(B)