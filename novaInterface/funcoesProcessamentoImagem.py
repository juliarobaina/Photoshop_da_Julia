import cv2
import numpy as np
from math import floor
from matplotlib import pyplot as plt #do histograma func


def escalaDeCinza(img_cv):
    b,g,r = cv2.split(img_cv)

    l, c = b.shape
   
    cinza = np.zeros(shape=(l,c))
    cinza = 0.11 * b + 0.59 * g + 0.3 * r
    cinza = cinza.astype(np.uint8)

    return cinza
    


#insere paddings zerados
def matrizComBordasZeradas(matriz, bordas, linhasMatrizImagem, colunasMatrizImagem):
    index = 0

    linhasMatrizZero = linhasMatrizImagem + (bordas * 2)
    colunasMatrizZero = colunasMatrizImagem + (bordas * 2)

    matrizZero = np.zeros(shape = (linhasMatrizZero,colunasMatrizZero)).astype(int)
   
    for i in range(bordas, linhasMatrizZero - bordas):
        matrizZero[i][bordas:colunasMatrizZero - bordas] = matriz[index]
        index += 1

    return matrizZero

def convolucao(filtered_img, matrizImagemParaFiltro, kernel, ordemKernel,linhasMatrizImagem, colunasMatrizImagem, divisor):

    for i in range(0, linhasMatrizImagem):
        z = 0

        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            
            soma = 0
            for p in range(0,ordemKernel):
                z = j
                for r in range(0,ordemKernel):
                    soma += (kernel[p][r] * matrizImagemParaFiltro[x][z])
                    #print(matrizImagemParaFiltro[p][r], end=' ')

                    z += 1
                #print()
                x += 1
            #print('-------------------------------------------')
            pixelNovo = abs(floor(soma / divisor)) 
           
            if pixelNovo > 255: #normalização, pixels variam de 0-255
                filtered_img[i][j] = 255
            else:
                filtered_img[i][j] = pixelNovo
   
    return filtered_img

def filtroMedia(tamanhoKernel:int, img_cv):    
    
    b,g,r = cv2.split(img_cv)
    
    linhasMatrizImagem, colunasMatrizImagem = r.shape    

    kernel, divisor = kernelMedia(tamanhoKernel)

    bordas = tamanhoKernel // 2

    matrizImagemParaFiltro = matrizComBordasZeradas(b, bordas, linhasMatrizImagem, colunasMatrizImagem)
    b = convolucao(b,matrizImagemParaFiltro,kernel,tamanhoKernel,linhasMatrizImagem,colunasMatrizImagem,divisor)

    matrizImagemParaFiltro = matrizComBordasZeradas(g, bordas, linhasMatrizImagem, colunasMatrizImagem)
    g = convolucao(g,matrizImagemParaFiltro,kernel,tamanhoKernel,linhasMatrizImagem,colunasMatrizImagem, divisor)

    matrizImagemParaFiltro = matrizComBordasZeradas(r, bordas, linhasMatrizImagem, colunasMatrizImagem)
    r = convolucao(r,matrizImagemParaFiltro,kernel,tamanhoKernel,linhasMatrizImagem,colunasMatrizImagem, divisor)
 
    return cv2.merge((b, g, r))
   
def filtroGaussiano(tamanhoKernel:int, img_cv):
    
    b,g,r = cv2.split(img_cv)
   
    linhasMatrizImagem, colunasMatrizImagem = r.shape 
    
    kernel, divisor = kernelGaussiano(tamanhoKernel)
    
    bordas = tamanhoKernel // 2
   
    matrizImagemParaFiltro = matrizComBordasZeradas(b, bordas, linhasMatrizImagem, colunasMatrizImagem)
    b = convolucao(b,matrizImagemParaFiltro,kernel,tamanhoKernel,linhasMatrizImagem,colunasMatrizImagem,divisor)

    matrizImagemParaFiltro = matrizComBordasZeradas(g, bordas, linhasMatrizImagem, colunasMatrizImagem)
    g = convolucao(g,matrizImagemParaFiltro,kernel,tamanhoKernel,linhasMatrizImagem,colunasMatrizImagem, divisor)

    matrizImagemParaFiltro = matrizComBordasZeradas(r, bordas, linhasMatrizImagem, colunasMatrizImagem)
    r = convolucao(r,matrizImagemParaFiltro,kernel,tamanhoKernel,linhasMatrizImagem,colunasMatrizImagem, divisor)
    
    return cv2.merge((b, g, r))

def matrizComBordasGemeas(matriz, bordas, linhasMatrizImagem, colunasMatrizImagem):
    matrizParaMediana = matrizComBordasZeradas(matriz, bordas, linhasMatrizImagem, colunasMatrizImagem)
    tamzL,tamzA = matrizParaMediana.shape 

    #valores das arestas
    matrizParaMediana[bordas-1][bordas - 1] = matriz[0][0]
    matrizParaMediana[(tamzL - bordas)][bordas-1] = matriz[linhasMatrizImagem - 1][0]
    matrizParaMediana[bordas-1][colunasMatrizImagem + bordas] = matriz[0][colunasMatrizImagem - 1]
    matrizParaMediana[(linhasMatrizImagem + bordas)][(colunasMatrizImagem + bordas)] = matriz[linhasMatrizImagem - 1][colunasMatrizImagem - 1]
    
    #valores das linhas entre as arestas
    matrizParaMediana[bordas - 1][bordas:tamzA - bordas] = matriz[0][:]
    matrizParaMediana[linhasMatrizImagem + bordas][bordas:tamzA - bordas] = matriz[linhasMatrizImagem - 1][:]

    index = 0

    #valores das colunas
    for i in range(bordas,linhasMatrizImagem+bordas):     
        matrizParaMediana[i][bordas - 1] = matrizParaMediana[i][bordas]
      
        matrizParaMediana[i][tamzA - bordas] = matriz[index][colunasMatrizImagem - 1] 

        index += 1
        if index == linhasMatrizImagem:
            index = 0
    
    #preenche as demais colunas
    index = 0
    for i in range(bordas,linhasMatrizImagem+bordas):
        for j in range(0, bordas - 1):
            matrizParaMediana[i][j] = matrizParaMediana[i][bordas]

            if i == bordas:
                matrizParaMediana[i - 1][j] = matrizParaMediana[i - 1][bordas - 1]
                matrizParaMediana[i - 1][(tamzA - bordas) + j + 1] = matrizParaMediana[i - 1][(tamzA - bordas) + j]
            if i == (linhasMatrizImagem + bordas) - 1:
                matrizParaMediana[linhasMatrizImagem + bordas][j] = matrizParaMediana[linhasMatrizImagem + bordas][bordas - 1]
                matrizParaMediana[linhasMatrizImagem + bordas][(tamzA - bordas) + j + 1] = matrizParaMediana[linhasMatrizImagem - 1][index]
            
            matrizParaMediana[i][(tamzA - bordas) + j + 1] = matriz[index][colunasMatrizImagem - 1]
           
        index += 1
        if index == linhasMatrizImagem - 1:
            index = 0
    
    index = 1
    
    while index < bordas:
        matrizParaMediana[:index][:] = matrizParaMediana[bordas - 1][:]
        matrizParaMediana[(linhasMatrizImagem + bordas + index)][:] = matrizParaMediana[linhasMatrizImagem + bordas][:]

        index += 1

    return matrizParaMediana

def mediana(matriz, matrizBordasGemeas, tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem):
    matrizMediana = np.zeros(shape = (tamanhoKernel * tamanhoKernel)).astype(int)
    
    for i in range(0, linhasMatrizImagem):
        z = 0

        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            ind = 0

            for _ in range(0,tamanhoKernel):
                z = j
               
                for _ in range(0,tamanhoKernel):
                    matrizMediana[ind] = matrizBordasGemeas[x][z]
                    ind += 1                
                    z += 1
            
                x += 1

            matrizMediana = np.sort(matrizMediana, kind= 'mergesort')
            mediana = np.median(matrizMediana).astype(int)
            matriz[i][j] = mediana

def filtroMediana(tamanhoKernel:int,img_cv):
    
    b,g,r = cv2.split(img_cv)

    linhasMatrizImagem, colunasMatrizImagem = r.shape 
    bordas = tamanhoKernel // 2
    
    matrizComBordasGemeasB = matrizComBordasGemeas(b, bordas, linhasMatrizImagem, colunasMatrizImagem)
    matrizComBordasGemeasG = matrizComBordasGemeas(g, bordas, linhasMatrizImagem, colunasMatrizImagem)
    matrizComBordasGemeasR = matrizComBordasGemeas(r, bordas, linhasMatrizImagem, colunasMatrizImagem)

  
    mediana(b,matrizComBordasGemeasB,tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem)
    mediana(g,matrizComBordasGemeasG,tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem)
    mediana(r,matrizComBordasGemeasR,tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem)

    return cv2.merge((b, g, r))


def kernelSobel(tamanho: int):

    if tamanho == 3:
        kernelHorizontal = np.array([[-1, -2, -1],
                                    [0, 0, 0],
                                    [1, 2, 1]
                                    ])
        kernelVertical = np.array([[-1, 0, 1],
                                    [-2, 0, 2],
                                    [-1, 0, 1]
                                    ])
    elif tamanho == 5:
        kernelVertical = np.array([[-1, -2, 0, 2, 1],
                                    [-4, -8, 0, 8, 4],
                                    [-6, -12, 0, 12, 6],
                                    [-4, -8, 0, 8, 4],
                                    [-1, -2, 0, 2, 1]
                                    ])
        kernelHorizontal = np.array([[-1, -4, -6, -4, -1],
                                    [-2, -8, -12, -8, -2],
                                    [0, 0, 0, 0, 0],
                                    [2, 8, 12, 8, 2],
                                    [1, 4, 6, 4, 1]
                                    ])
    elif tamanho == 7:
        kernelVertical = np.array([[-1, -2, -3, 0, 3, 2, 1],
                                    [-4, -8, -12, 0, 12, 8, 4],
                                    [-6, -12, -18, 0, 18, 12, 6],
                                    [-4, -8, -12, 0, 12, 8, 4],
                                    [-1, -2, -3, 0, 3, 2, 1]
                                    ])
        kernelHorizontal = np.array([[-1, -4, -6, -4, -1, 0, 1],
                                    [-2, -8, -12, -8, -2, 0, 2],
                                    [-3, -12, -18, -12, -3, 0, 3],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [3, 12, 18, 12, 3, 0, -3],
                                    [2, 8, 12, 8, 2, 0, -2],
                                    [1, 4, 6, 4, 1, 0, -1]
                                    ])
   
    return kernelHorizontal, kernelVertical

def kernelMedia(tamanho:int):
    if tamanho == 3:
        kernel = np.array([
                        [1,1,1],
                        [1,1,1],
                        [1,1,1]
                        ])
        divisor = 9
    
    elif tamanho == 5:
        kernel = np.array([
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1]
                        ])
        divisor = 25
    
    elif tamanho == 7:
        kernel = np.array([
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1]
                        ])
        divisor = 49
    
    else:
        print(f'O kernel de tamanho {tamanho} não foi encontrado')
        exit()

    return kernel, divisor

def kernelGaussiano(tamanho:int):
    if tamanho == 3:
        kernel = np.array([[1, 2, 1],
                  [2, 4, 2],
                  [1, 2, 1]])
        divisor = 16

    elif tamanho == 5:
        kernel = np.array([[1, 4, 7, 4, 1],
                  [4, 16, 26, 16, 4],
                  [7, 26, 41, 26, 7],
                  [4, 16, 26, 16, 4],
                  [1, 4, 7, 4, 1]
                ])
        divisor = 273

    elif tamanho == 7:
        kernel = np.array([
                [1, 6, 15, 20, 15, 6, 1],
                [6, 36, 90, 120, 90, 36, 6],
                [15, 90, 225, 300, 225, 90, 15],
                [20, 120, 300, 400, 300, 120, 20],
                [15, 90, 225, 300, 225, 90, 15],
                [6, 36, 90, 120, 90, 36, 6],
                [1, 6, 15, 20, 15, 6, 1]                  
                ])
        divisor = 4096
    else:
        print(f'O kernel de tamanho {tamanho} não foi encontrado')
        exit()
    
    return kernel, divisor

def kernelLaplaciano(tamanho:int):
    if tamanho == 3:
        kernel = np.array([[-1, -1, -1],
                      [-1, 8, -1],
                      [-1, -1, -1]])
    elif tamanho == 5:
        kernel = np.array([[0, 1, 1, 1, 0],
                           [1,-1, -2, -1, 1],
                           [1, -2, -4, -2, 1],
                           [1, -1, -2, -1, 1],
                           [0, 1, 1, 1, 0]])

    elif tamanho == 7:
        kernel = np.array([[0, 0, 1, 1, 1, 0, 0],
                           [0, 1, 2, 2, 2, 1, 0],
                           [1, 2, 4, 8, 4, 2, 1],
                           [1, 2, 8, -24, 8, 2, 1],
                           [1, 2, 4, 8, 4, 2, 1],
                           [0, 1, 2, 2, 2, 1, 0],
                           [0, 0, 1, 1, 1, 0, 0]])
    
    return kernel

def filtroSobel(tamanho:int, img_cv):

    imgGaussiano = filtroGaussiano(3, img_cv)

    matrizCinza = escalaDeCinza(imgGaussiano)
   
    linhasMatrizImagem, colunasMatrizImagem = matrizCinza.shape 
    
    kernelHorizontal, kernelVertical = kernelSobel(tamanho)
   
    ordemMatrizKernel = 3
    bordas = ordemMatrizKernel // 2
    divisao = 1
   
    auxCinza = np.zeros(shape=(linhasMatrizImagem,colunasMatrizImagem)).astype(int)
    for i in range (0,linhasMatrizImagem):
        for j in range(0, colunasMatrizImagem):
            auxCinza[i][j] = matrizCinza[i][j]

    matrizImagemParaFiltroB = matrizComBordasZeradas(matrizCinza, bordas, linhasMatrizImagem, colunasMatrizImagem)
    b = convolucao(auxCinza,matrizImagemParaFiltroB,kernelHorizontal,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem,divisao)
    
    matrizImagemParaFiltroC = matrizComBordasZeradas(matrizCinza, bordas, linhasMatrizImagem, colunasMatrizImagem)
    c = convolucao(matrizCinza,matrizImagemParaFiltroC,kernelVertical,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem,divisao)

    for i in range (0,linhasMatrizImagem):
        for j in range(0, colunasMatrizImagem):
            if b[i][j] + c[i][j] > 255:
                matrizCinza[i][j] = 255
            else:
                matrizCinza[i][j] = b[i][j] + c[i][j]
   
    return matrizCinza

def filtroLaplaciano(tamanho:int, img_cv):
    imgGaussiano = filtroGaussiano(3, img_cv)

    matrizCinza = escalaDeCinza(imgGaussiano)

    linhasMatrizImagem, colunasMatrizImagem = matrizCinza.shape 
    
    kernel = kernelLaplaciano(tamanho)
   
    ordemMatrizKernel = 3
    bordas = ordemMatrizKernel // 2
  
    divisao = 1
   
    matrizImagemParaFiltro = matrizComBordasZeradas(matrizCinza, bordas, linhasMatrizImagem, colunasMatrizImagem)
    b = convolucao(matrizCinza,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem,divisao)
   
    return b
    
def binarizacao(usuarioT, matrizCinza):
    
   
    linhasMatriz, colunasMatriz = matrizCinza.shape 
    t = usuarioT
    for i in range(0, linhasMatriz):
            for j in range(0, colunasMatriz):
                if matrizCinza[i][j] > t: 
                    matrizCinza[i][j] = 0
                else:
                    matrizCinza[i][j] = 255
    
    return matrizCinza

def limiarizacaoGlobal(usuarioT:int, matriz, linhasMatriz, colunasMatriz):
   
    criterioParada = 256
   
    t = np.mean(matriz) #valor de thredshold
        
    while(criterioParada > usuarioT): #
        
        g1 = 0 #valores maiores que t
        g1 = np.uint(g1)
        g2 = 0 #valores menores ou iguais a t
        g2 = np.uint(g2)
        tamG1 = 0
        tamG2 = 0

        for i in range(0, linhasMatriz):
            for j in range(0, colunasMatriz):
                if matriz[i][j] > t:
                    g1 += matriz[i][j]
                    tamG1 += 1
                else:
                    g2 += matriz[i][j]
                    tamG2 += 1
                   

        
        if g1 == 0:
            u1 = 0
        else:
            u1 = g1 / tamG1
        if g2 == 0:
            u2 = 0
        else:
            u2 = g2 / tamG2
            
        novoT = (u1 + u2) / 2
        novoT = novoT
       
        criterioParada = abs(t - novoT)
        
        t = novoT
       

    imagem = binarizacao(t,matriz)
    return imagem

def metodoOtsu(matrizCinza):
     
    linhasMatriz, colunasMatriz = matrizCinza.shape 

    intensidades = np.zeros(shape=(256),dtype=float)#0-255
    
    for i in range(0,linhasMatriz):
        for j in range(0,colunasMatriz):
            intensidades[matrizCinza[i][j]] += 1 #Ex: o valor 255 apareceu 20x, intensidades[255] += 1 vinte vezes
    
    dic = {}
   
    #normalizando o histograma (Pi)
    for i in range(0,256):
        intensidades[i] /= (linhasMatriz * colunasMatriz)
        if intensidades[i] != 0:
            dic[i] = intensidades[i]
          
    tamanhoDic = 0
    for key in dic.keys():
        tamanhoDic+=1
   
    vetorFreq = np.zeros(shape=(tamanhoDic),dtype=float)
    vetorVal = np.zeros(shape=(tamanhoDic),dtype=float)
    cont = 0

    for key in dic.keys():
        vetorFreq[cont] = dic[key] #frequência
        vetorVal[cont] = key #valor
        cont+=1

    N = vetorFreq.sum()
    maior = 0
    t = 0
    for i in range(0, len(vetorVal)):
        if i == 0:
            wb = 0
            ub = 0
            wf = vetorFreq.sum() / N
            somaPonderada = 0
            for j in range(0, len(vetorFreq)):
                somaPonderada += vetorFreq[j] * vetorVal[j]
            uf = somaPonderada / vetorFreq.sum()
            sigma = wb * wf * pow((ub - uf), 2)
            if sigma > maior:
                maior = sigma
                t = vetorVal[i]
        else:
            wf = vetorFreq[i:len(vetorFreq)].sum() / N
            wb = vetorFreq[0:i].sum() / N
            somaPonderada = 0

            for j in range(i, len(vetorFreq)):
                somaPonderada += vetorFreq[j] * vetorVal[j]
            uf = somaPonderada / vetorFreq[i:len(vetorFreq)].sum()

            somaPonderada = 0
            for j in range(0, i):
                somaPonderada += vetorFreq[j] * vetorVal[j]
            ub = somaPonderada / vetorFreq[0:i].sum()

            sigma = wb * wf * pow((ub - uf), 2)

            if sigma > maior:
                maior = sigma
                t = vetorVal[i]
    
    imagem = binarizacao(t,matrizCinza)
    return imagem


#sem padding quando envia pro otsu e binarização
def limiarizacaoAdaptativaSemPaddingOtsu(matriz, janela):


    matriz = escalaDeCinza(matriz)
    linhasMatrizImagem, colunasMatrizImagem = matriz.shape   
    
    bordas = janela // 2
    matrizBordas = matrizComBordasZeradas(matriz, bordas, linhasMatrizImagem, colunasMatrizImagem)
  
    lb,cb = matrizBordas.shape
    
   
    i = bordas
    j = 0
    cc = 0
    cc2 = 0
    pi = janela
    po = bordas + abs(bordas - janela)
    t = 0
    matrizNova = np.zeros(shape=(linhasMatrizImagem,colunasMatrizImagem),dtype=matriz.dtype)#acho que essa foi pra sem bordas

    while cc2 < lb - bordas:
        p = j + bordas
        
        while cc < cb - bordas:
            a = matrizBordas[i:po, p:pi]
            
            matrizNova[i-bordas:po-bordas, p-bordas:pi-bordas] = metodoOtsu(a)
          
            p = pi
            cc = p
            j += bordas
            pi += janela
            
            if pi > cb - bordas:
                pi = cb - bordas
        
        i = po
        po = i + janela
        if po > lb - bordas:
                po = lb - bordas
        j = 0
        cc = 0
        cc2 = i
        pi = janela
   
    return matrizNova




def maiorDivisorComum(a, b):
    divisor = np.gcd(a, b)
    if divisor == a or divisor == b:
        for i in range(divisor - 1, 0, -1):
            if a % i == 0 and b % i == 0:
                return i
    return divisor

def limiarizacaoAdaptativaMedia(matriz, janela, c):
    
    linhasMatrizImagem, colunasMatrizImagem = matriz.shape   
    #print(f'window {janela}')
    #print(f'c {c}')
    c = c
    
    for j in range(0, linhasMatrizImagem,janela):
        for k in range(0, colunasMatrizImagem,janela):

            if matriz[j:j+janela,k:k+janela].shape[0] < janela or matriz[j:j+janela,k:k+janela].shape[1] < janela:
                mdc = maiorDivisorComum(matriz[j:j+janela,k:k+janela].shape[0],matriz[j:j+janela,k:k+janela].shape[1])
                if mdc != 1:
                    for l in range(0, matriz[j:j+janela,k:k+janela].shape[0],mdc):
                        for m in range(0, matriz[j:j+janela,k:k+janela].shape[1],mdc):
                            
                            pixelNovo = np.mean(matriz[l:l+mdc,m:m+mdc])
                            threshold = pixelNovo - c
                            matriz[l:l+mdc,m:m+mdc] = binarizacao(threshold,matriz[l:l+mdc,m:m+mdc])
                else:
                    pixelNovo = np.mean(matriz[j:j+janela,k:k+janela])
                    threshold = pixelNovo - c
                    matriz[j:j+janela,k:k+janela] = binarizacao(threshold,matriz[j:j+janela,k:k+janela])
            else:
                pixelNovo = np.mean(matriz[j:j+janela,k:k+janela])
                threshold = pixelNovo - c
                matriz[j:j+janela,k:k+janela] = binarizacao(threshold,matriz[j:j+janela,k:k+janela])
    return matriz

def limiarizacaoAdaptativaMBernsen(matriz, janela):
    linhasMatrizImagem, colunasMatrizImagem = matriz.shape   
    
    
    for j in range(0, linhasMatrizImagem,janela):
        for k in range(0, colunasMatrizImagem,janela):
           
            if matriz[j:j+janela,k:k+janela].shape[0] < janela or matriz[j:j+janela,k:k+janela].shape[1] < janela:
                mdc = maiorDivisorComum(matriz[j:j+janela,k:k+janela].shape[0],matriz[j:j+janela,k:k+janela].shape[1])
                if mdc != 1:
                    for l in range(0, matriz[j:j+janela,k:k+janela].shape[0],mdc):
                        for m in range(0, matriz[j:j+janela,k:k+janela].shape[1],mdc):
                            
                            min, max = np.float64(np.min(matriz[l:l+mdc,m:m+mdc])), np.float64(np.max(matriz[l:l+mdc,m:m+mdc]))
                            
                            threshold = np.float64((min + max) / 2)
                            matriz[l:l+mdc,m:m+mdc] = binarizacao(threshold,matriz[l:l+mdc,m:m+mdc])
                else:
                    min, max = np.float64(np.min(matriz[j:j+janela,k:k+janela])), np.float64(np.max(matriz[j:j+janela,k:k+janela]))
                    threshold = np.float64((min + max) / 2)
                    matriz[j:j+janela,k:k+janela] = binarizacao(threshold,matriz[j:j+janela,k:k+janela])
            else:
                min, max = np.float64(np.min(matriz[j:j+janela,k:k+janela])), np.float64(np.max(matriz[j:j+janela,k:k+janela]))
                threshold = np.float64((min + max) / 2)
                matriz[j:j+janela,k:k+janela] = binarizacao(threshold,matriz[j:j+janela,k:k+janela])
       
    return matriz


def dilatacao(matriz, janela):

    linhasMatrizImagem, colunasMatrizImagem = matriz.shape   
    
    
    elementoEstruturante = np.full((janela, janela), 255)#é pq meu foreground é preto e background branco
   
   

    bordas = elementoEstruturante.shape[0] // 2
    matrizBordas = matrizComBordasZeradas(matriz, bordas, linhasMatrizImagem, colunasMatrizImagem)
  
    for i in range(0, linhasMatrizImagem):
        z = 0

        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            
            sai = 0
            for p in range(0,elementoEstruturante.shape[0]):
                if sai == 1:
                    break
                z = j
                for r in range(0,elementoEstruturante.shape[0]):
                    if elementoEstruturante[p][r] == matrizBordas[x][z]:#hit
                        matriz[i][j] = 255
                        sai = 1
                        break

                    z += 1
              
                x += 1
            if sai == 0:
                matriz[i][j] = 0
         
   
    return matriz

def erosao(matriz, janela):

    #print(matriz)

    linhasMatrizImagem, colunasMatrizImagem = matriz.shape  
     
    
    elementoEstruturante = np.full((janela, janela), 255) #é pq meu foreground é preto e background branco
    bordas = elementoEstruturante.shape[0] // 2
    matrizBordas = matrizComBordasZeradas(matriz, bordas, linhasMatrizImagem, colunasMatrizImagem)
   
    for i in range(0, linhasMatrizImagem):
        z = 0

        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            
            sai = 0
            for p in range(0,elementoEstruturante.shape[0]):
                if sai == 1:
                    break
                z = j
                for r in range(0,elementoEstruturante.shape[0]):
                    if elementoEstruturante[p][r] != matrizBordas[x][z]:#fit
                        matriz[i][j] = 0
                        sai = 1
                        break
                    

                    z += 1
              
                x += 1
            if sai == 0:
                matriz[i][j] = 255
         
    return matriz

def abertura(matriz, janela):
    imgErosao = erosao(matriz, janela)
    imgDilatacao = dilatacao(imgErosao, janela)
    return imgDilatacao

def fechamento(matriz, janela):
    imgDilatacao = dilatacao(matriz, janela)
    imgErosao = erosao(imgDilatacao, janela)
    return imgErosao



