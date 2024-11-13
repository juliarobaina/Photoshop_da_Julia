import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
from math import floor
from matplotlib import pyplot as plt#do histograma func

def load_image():
    global img_cv
    file_path = filedialog.askopenfilename()
    if file_path:
        img_cv = cv2.imread(file_path)
        display_image(img_cv, original=True)  # Exibe a imagem original
        refresh_canvas()

def display_image(img, original=False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    global img_pil
    img_pil = Image.fromarray(img_rgb)
    
    # Obtém o tamanho da imagem original
    img_width, img_height = img_pil.size
    
    # Redimensional a imagem para caber no canvas se for muito grande
    max_size = 500
    img_pil.thumbnail((max_size, max_size))  # Maintain aspect ratio
    img_tk = ImageTk.PhotoImage(img_pil)

    # Calcula a posição para centralizar a imagem dentro do canvas se for menor
    canvas_width, canvas_height = max_size, max_size
    x_offset = (canvas_width - img_pil.width) // 2
    y_offset = (canvas_height - img_pil.height) // 2

    if original:
        original_image_canvas.delete("all")  # Limpa a canvas
        original_image_canvas.image = img_tk  # Mantém a referência viva - garbage collection
        original_image_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=img_tk)
    else:
        edited_image_canvas.delete("all")  # Limpa a canvas
        edited_image_canvas.image = img_tk
        edited_image_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=img_tk)
        

def escalaDeCinza(img):
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
                    print(matrizImagemParaFiltro[p][r], end=' ')

                    z += 1
                print()
                x += 1
            print('-------------------------------------------')
            pixelNovo = abs(floor(soma / divisor)) 
           
            if pixelNovo > 255: #normalização, pixels variam de 0-255
                filtered_img[i][j] = 255
            else:
                filtered_img[i][j] = pixelNovo
   
    return filtered_img

def filtroMedia(tamanhoKernel:int):    
    
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
   
def filtroGaussiano(tamanhoKernel:int):
    
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

def filtroMediana(tamanhoKernel:int):
    
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


def kernelSobel():
    
    kernelHorizontal = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]
                    ])
    kernelVertical = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]
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

def kernelLaplaciano():
    kernel = np.array([[-1, -1, -1],
                      [-1, 8, -1],
                      [-1, -1, -1]])
    return kernel

def filtroSobel():
    imgGaussiano = filtroGaussiano(3)

    matrizCinza = escalaDeCinza(imgGaussiano)
   
    linhasMatrizImagem, colunasMatrizImagem = matrizCinza.shape 
    
    kernelHorizontal, kernelVertical = kernelSobel()
   
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

def filtroLaplaciano():
    imgGaussiano = filtroGaussiano(3)

    matrizCinza = escalaDeCinza(imgGaussiano)

    linhasMatrizImagem, colunasMatrizImagem = matrizCinza.shape 
    
    kernel = kernelLaplaciano()
   
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

def limiarizacaoGlobal(usuarioT:int, matriz,linhasMatriz, colunasMatriz):
   
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

def limiarizacaoAdaptativaMedia(matriz, janela):
    
    linhasMatrizImagem, colunasMatrizImagem = matriz.shape   
    
    c = 6
    
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



def apply_filter(filter_type):
    if img_cv is None:
        return
    
    match filter_type:
        case 'media3':
            matrizCinza = escalaDeCinza(img_cv)
            #t = limiarizacaoGlobal(37,matrizCinza,matrizCinza.shape[0],matrizCinza.shape[1])
            A = limiarizacaoAdaptativaMBernsen(matrizCinza,71)
            filtered_img = erosao(matrizCinza,3)
            #aux = teste(img_cv,5)
            #print('segmentada')
            #print(aux)
            #filtered_img = dilatacao(aux,3)
           # filtered_img = metodoOtsu(matrizCinza)
            #g = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            #matrizCinza = escalaDeCinza(img_cv)
            #filtered_img = cv2.adaptiveThreshold(matrizCinza,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,255,10)
            #t,filtered_img=cv2.threshold(g,255,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
            #histograma()
           # filtered_img = binarizacao(metodoOtsu(img_cv), img_cv)
            #aux = cv2.adaptiveThreshold(matrizCinza,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,8)
            #kernel = np.ones((55,55), np.uint8)
            #filtered_img = cv2.dilate(aux,kernel,iterations=1)
            #filtered_img = teste(img_cv,21)
            ''' matrizCinza = escalaDeCinza(img_cv)
            janela=3
            ppp = np.full((janela,janela),0,np.uint8)
              #for i in range (0,janela):
                #for j in range(floor(janela/2),janela-1):
                  #  ppp[i][j] = 255
            for i in range (floor(janela/2),janela-1):
                for j in range(0,janela):
                    ppp[i][j] = 255
            kernel = np.ones((3,3), np.uint8)
            aux = cv2.adaptiveThreshold(matrizCinza,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,255,10)
            print(aux)
            #di = cv2.dilate(aux,ppp,iterations=1)
            filtered_img = cv2.erode(aux,ppp,iterations=1)'''
            '''
            1)convoluir a imagem com kernel media
            2)convoluida - original
            3)faz limiarização com o valor de c. c é o threshold
            4)inverte, o que for 1 vira 0, o que for 0 vira 1
            '''
            ''' 
             a = a.astype(np.uint8)
            
            t,filtered_img=cv2.threshold(a,255,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
            '''
        case 'media5':
            filtered_img = filtroMedia(5)

        case 'media7':
            filtered_img = filtroMedia(7)

        case 'gaussiano3':
            filtered_img = filtroGaussiano(3)

        case 'gaussiano5':
            filtered_img = filtroGaussiano(5)

        case 'gaussiano7':
            filtered_img = filtroGaussiano(7)

        case 'mediana3':
            filtered_img = filtroMediana(3)

        case 'mediana5':
            filtered_img = filtroMediana(5)

        case 'mediana7':
            filtered_img = filtroMediana(7)

        case 'sobel':
            filtered_img = filtroSobel()

        case 'laplaciano':
            filtered_img = filtroLaplaciano()
        
    display_image(filtered_img, original=False)  # Exibe a imagem editada

def refresh_canvas():
    edited_image_canvas.delete("all")  # Limpa a canvas para exibir a nova imagem


def salvarImagem():
        
    if img_pil is None:
        popup = tk.Toplevel()
        popup.geometry("240x60")
        popup.resizable(0,0)
        popup.wm_title('Operação Inválida')
        label = tk.Label(popup, text='Operação Inválida, Edite a imagem')
        label.grid(row=0,column=3)
    
    else:
        nomeArquivo = filedialog.asksaveasfile(mode='w', defaultextension='jpg')
   
        if nomeArquivo is None:
            return
   
        img_pil.save(nomeArquivo)


# Função para atualizar o valor do slider enquanto ele é movido
def atualizar_valor(valor, label):
    label.config(text=f'Valor Atual: {valor}')

# Função para atualizar o valor do slider enquanto ele é movido
def atualizar_valorC(valor, label):
    label.config(text=f'Valor Atual C: {valor}')

# Função para lidar com o evento de soltura do mouse
def on_slider_release(slider):
      # Chama a função para calcular a média ou outro cálcul
    mc = escalaDeCinza(img_cv)
    t,filtered_img = cv2.threshold(mc,255,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    kernel = np.ones((30,30), np.uint8)
    A = cv2.dilate(filtered_img,kernel,iterations=1)
    A = cv2.erode(A,kernel,iterations=1)
    #A = limiarizacaoAdaptativaMBernsen(mc,71)
    #B = binarizacao(A,mc)
    #C = fechamento(A,slider)
    #A = binarizacao(t,mc)
    display_image(A, original=False) 
   # display_image(erosao(A,9), original=False)  # Exibe a imagem editada

# Função para criar o slider e os labels dentro de um popup
# Função para aumentar o valor do slider ao pressionar a seta para a direita
def aumentar_slider(event, slider, label):
    novo_valor = slider.get() + 1
    if novo_valor <= slider.cget("to"):  # Limita o valor máximo
        slider.set(novo_valor)
        atualizar_valor(novo_valor, label)

# Função para diminuir o valor do slider ao pressionar a seta para a esquerda
def diminuir_slider(event, slider, label):
    novo_valor = slider.get() - 1
    if novo_valor >= slider.cget("from"):  # Limita o valor mínimo
        slider.set(novo_valor)
        atualizar_valor(novo_valor, label)
def criar_popup():
    # Criando a janela popup (Toplevel)
    popup = tk.Toplevel()
    popup.title("Slider em Popup")
    popup.geometry("500x500")

     # Criando o slider
    slider = tk.Scale(popup, from_=1, to=255, orient="horizontal", command=lambda val: [atualizar_valor(val, label), on_slider_release(int(val))], length=400)
    slider.pack(pady=20)

    # Criando o label para mostrar o valor atual
    label = tk.Label(popup, text="Valor Atual: 0")
    label.pack()

     # Criando o slider
    slider2 = tk.Scale(popup, from_=1, to=255, orient="horizontal", command=lambda val: [atualizar_valorC(val, label2), on_slider_release(int(val))], length=400)
    slider2.pack(pady=20)
    
    
    # Criando o label para mostrar o valor atual
    label2 = tk.Label(popup, text="Valor Atual C: 0")
    label2.pack()

    # Bind das teclas de seta para aumentar ou diminuir o valor do slider
    popup.bind("<Right>", lambda event: aumentar_slider(event, slider, label))  # seta para a direita
    popup.bind("<Left>", lambda event: diminuir_slider(event, slider, label))   # seta para a esquerda

    # Usando o comando para atualizar o valor enquanto o slider é movido
  #  slider.config(command=lambda val: on_slider_release(int(val)) )
'''
    # Criando o slider
    slider = tk.Scale(popup, from_=1, to=255, orient="horizontal", command=lambda val: atualizar_valor(val, label))
    slider.pack()
    
    # Criando o label para mostrar o valor atual
    label = tk.Label(popup, text="Valor Atual: 0")
    label.pack()

    # Criando o label para mostrar o resultado do cálculo (exemplo: média)
    label_resultado = tk.Label(popup, text="Média Calculada: 0")
    label_resultado.pack()

    # Bind do evento ButtonRelease-1 ao slider (quando o mouse é solto)
    slider.bind("<ButtonRelease-1>", lambda event: on_slider_release(slider.get()))
'''
    

# Definindo a GUI
root = tk.Tk()
root.title("Photoshop da Julia")

# Define o tamanho da janela da aplicação 1200x800
root.geometry("1085x550")

# Define a cor de fundo da janela
root.config(bg="#2e2e2e")

img_cv = None
img_pil = None
# Cria o menu da aplicação
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

#carregar imagem # File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Carregar Imagem", command=load_image)
file_menu.add_command(label="Salvar Imagem", command=salvarImagem)
file_menu.add_command(label="Criar Valoresm", command=criar_popup)

#file_menu.add_separator()
#file_menu.add_command(label="Exit", command=root.quit)

#Filtros Passa-Baixa
media_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Filtro Média", menu=media_menu)
media_menu.add_command(label="3x3", command=lambda: apply_filter("media3"))
media_menu.add_command(label="5x5", command=lambda: apply_filter("media5"))
media_menu.add_command(label="7x7", command=lambda: apply_filter("media7"))

gaussiano_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Filtro Gaussiano", menu=gaussiano_menu)
gaussiano_menu.add_command(label="3x3", command=lambda: apply_filter("gaussiano3"))
gaussiano_menu.add_command(label="5x5", command=lambda: apply_filter("gaussiano5"))
gaussiano_menu.add_command(label="7x7", command=lambda: apply_filter("gaussiano7"))

mediana_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Filtro Mediana", menu=mediana_menu)
mediana_menu.add_command(label="3x3", command=lambda: apply_filter("mediana3"))
mediana_menu.add_command(label="5x5", command=lambda: apply_filter("mediana5"))
mediana_menu.add_command(label="7x7", command=lambda: apply_filter("mediana7"))

#Para Filtro Passa-Alta
menu_bar.add_command(label="Filtro Sobel", command=lambda: apply_filter("sobel"))
menu_bar.add_command(label="Filtro Laplaciano", command=lambda: apply_filter("laplaciano"))



# Cria a canvas para a imagem original com borda (sem background)
original_image_canvas = tk.Canvas(root, width=500, height=500, bg="#2e2e2e", highlightthickness=1, highlightbackground="white")
original_image_canvas.grid(row=0, column=0, padx=20, pady=20)

# Cria a canvas para a imagem editada com borda (sem background)
edited_image_canvas = tk.Canvas(root, width=500, height=500, bg="#2e2e2e", highlightthickness=1, highlightbackground="white")
edited_image_canvas.grid(row=0, column=1, padx=20, pady=20)

root.mainloop()
