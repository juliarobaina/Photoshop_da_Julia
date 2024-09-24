#teste para criar filtros passa-baixa e passa-alta com máscaras de convolução
import numpy as np




matrizImagem = np.array([[1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1]])

linhasMatrizImagem = 12
colunasMatrizImagem= 10

kernel = np.array([[2,2,2],
                  [2,2,2],
                  [2,2,2],
                  ])

linhasKernel = 3
colunasKernel = 3
ordemMatrizKernel = 3
bordas = ordemMatrizKernel // 2 #pega o piso da divisão

auxVetor = np.array([[0,0,0,0,0],
                    [0,1,1,1,0],
                    [0,1,1,1,0],
                    [0,0,0,0,0]])

ini_array = np.array([[1, 2, 3], [45, 4, 7], [9, 6, 10]])


# Array to be added as column
#ini_array = np.append(ini_array,0)
#matrizZero = np.zeros(shape=(linhasKernel+(bordas*2),colunasKernel+(bordas*2))).astype(int)

def matrizComBordasZeradas(matriz, matrizZero, bordas, tamanhoMatrizZero):
    #código pra preencher a matriz auxiliar iniciado
    index = 0
    #print(f'matriz zero {linhasMatrizZero[0]} {type(linhasMatrizZero[1])}')

    linhasMatrizZero = tamanhoMatrizZero[0]
    colunasMatrizZero = tamanhoMatrizZero[1]
   # l = linhasMatrizZero[0]
    #print(type(linhasMatrizZero[0]))
    #print(f'bordas {bordas}, linhas+bordas{linhasKernel+bordas}')
    for i in range(bordas, linhasMatrizZero-bordas):#tava linhas+bordas
        #print(abs(rowIni-(bordas*2)))
        #print(colIni+bordas)
        #print(f'i repete {i}')
       # print(f'matrizZero[{i}][{bordas}:{colunasMatrizZero - bordas}] = matriz[{index}]')
        matrizZero[i][bordas:colunasMatrizZero - bordas] = matriz[index]#1:4
        index += 1
    return matrizZero

#matrizImagemParaFiltro = matrizComBordasZeradas(ini_array, matrizZero, bordas, linhasKernel, colunasKernel)
#print(matrizImagemParaFiltro)
#exit()
#código pra preencher a matriz auxiliar finalizado

#ini_array = np.append(ini_array,0)
#zero[1:-1, 1:-1] = ini_array
#np.insert(zero, 1, ini_array, axis=1).reshape(4,4)
#for i in range(0,3):
 #   print(np.concatenate(([9],ini_array[i],[9])))

# Adding column to array using append() method
#arr = np.insert(ini_array, 0, column_to_be_added, axis=1)
matrizZero = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)
#print(matrizZero)
matrizImagemParaFiltro = matrizComBordasZeradas(matrizImagem, matrizZero, bordas, matrizZero.shape)
print(matrizImagemParaFiltro)
exit()
def filtroConvolucao(matrizImagem, matrizImagemParaFiltro, kernel, ordemKernel,linhasMatrizImagem, colunasMatrizImagem):

    #tam = 3 #coluna limite (tam - 1) que o kernel vai estar, é a ordem do kernel
    #z = 0
    #x = 0
    #soma = 0
    #B = np.zeros(shape=(2, 3)).astype(int) #astype trnasforma os valores para int --np.int64--

    for i in range(0, linhasMatrizImagem):
        z = 0
        #tam = 3
        #print(f'Estou no print do i z={z} e tam={tam}')
        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            #print(f'Estou no print do j z={z} e x={x}')
            soma = 0
            for p in range(0,ordemKernel):
                z = j
                for r in range(0,ordemKernel):
                # print(f'Estou no print do r M[{p}][{r}] * AUX[{x}][{z}]')
                    #soma += 1
                    #print(f'kernel[{p}][{r}] = {kernel[p][r]} + auxVetor[{x}][{z}] = {matrizImagemParaFiltro[x][z]}')
                    soma += kernel[p][r] * matrizImagemParaFiltro[x][z]
                    z += 1
                    #print(f'Estou no print do r z={z}')
            
                x += 1
                #print(f'Estou no print do p x={x}')
            #print(f'soma = {soma}')
            #tam += 1
            #print(f'Estou no print do j tam={tam}')
            if soma > 255: #normalização, pixels variam de 0-255
                soma = 255
            matrizImagem[i][j] = soma #usar matriz original em vez de B
            #print(f'B[{i}{j}] = {soma}')

print(f'Matriz resultante')
print(matrizImagem)