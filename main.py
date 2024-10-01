import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
from math import floor

def load_image():
    global img_cv
    file_path = filedialog.askopenfilename()
    if file_path:
        img_cv = cv2.imread(file_path)
        display_image(img_cv, original=True)  # Exibe a imagem original
        refresh_canvas()

def display_image(img, original=False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    
    # Obtém o tamanho da imagem orifinal
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
        edited_image_canvas.delete("all")  # Limapa a canvas
        edited_image_canvas.image = img_tk
        edited_image_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=img_tk)




def matrizComBordasZeradas(matriz, matrizZero, bordas, tamanhoMatrizZero):
    index = 0

    linhasMatrizZero = tamanhoMatrizZero[0]
    colunasMatrizZero = tamanhoMatrizZero[1]
  
    for i in range(bordas, linhasMatrizZero-bordas):
        matrizZero[i][bordas:colunasMatrizZero - bordas] = matriz[index]
        index += 1
    return matrizZero

def convolucao(filtered_img, matrizImagemParaFiltro, kernel, ordemKernel,linhasMatrizImagem, colunasMatrizImagem, divisao):

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
                    
                    z += 1
               
                x += 1
            
            pixelNovo = floor(soma / divisao)
            #print(pixelNovo)
              #usar matriz original em vez de B. De acordo com 1 vídeo é a soma dividido pelo 1/9 por exemplo soma * (1/9)
            if pixelNovo > 255: #normalização, pixels variam de 0-255
                filtered_img[i][j] = 255
            elif pixelNovo < 0:
                 filtered_img[i][j] = 0
            else:
                filtered_img[i][j] = pixelNovo
    #print(f'dentro da função filtr \n {filtered_img}')
    print(filtered_img)
    return filtered_img

def filtroMedia(tamanhoFiltro:int):#blur
    
    b,g,r = cv2.split(img_cv)
 
    '''b_novo = np.zeros_like(b)
    g_novo = np.zeros_like(g)
    r_novo = np.zeros_like(r)'''
    
    #tamImagem = img_cv.shape
    
    #linhasMatrizImagem, colunasMatrizImagem = r_novo.shape    
    linhasMatrizImagem, colunasMatrizImagem = r.shape    


    if tamanhoFiltro == 3:
        kernel = np.array([
                        [1,1,1],
                        [1,1,1],
                        [1,1,1]
                        ])
        
        ordemMatrizKernel = 3
        bordas = ordemMatrizKernel // 2 #tanto faz linha ou coluna
        divisao = 9
        
        matrizZero = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)

        matrizImagemParaFiltro = matrizComBordasZeradas(b, matrizZero, bordas, matrizZero.shape)
        b = convolucao(b,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem,divisao)

        matrizImagemParaFiltro = matrizComBordasZeradas(g, matrizZero, bordas, matrizZero.shape)
        g = convolucao(g,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem, divisao)

        matrizImagemParaFiltro = matrizComBordasZeradas(r, matrizZero, bordas, matrizZero.shape)
        r = convolucao(r,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem, divisao)
        
        return cv2.merge((b, g, r))
    
        
    elif tamanhoFiltro == 5:
        pass
    elif tamanhoFiltro == 7:
        kernel = np.array([
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1]
                        ])
        ordemMatrizKernel = 7
        bordas = ordemMatrizKernel // 2 #tanto faz linha ou coluna
        divisao = 49
        
        matrizZero = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)

        matrizImagemParaFiltro = matrizComBordasZeradas(b, matrizZero, bordas, matrizZero.shape)
        b = convolucao(b,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem,divisao)

        matrizImagemParaFiltro = matrizComBordasZeradas(g, matrizZero, bordas, matrizZero.shape)
        g = convolucao(g,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem, divisao)

        matrizImagemParaFiltro = matrizComBordasZeradas(r, matrizZero, bordas, matrizZero.shape)
        r = convolucao(r,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem, divisao)
        
        return cv2.merge((b, g, r))
    else:
        print('entrada inválida')
    
def filtroGaussiano(tamanhoFiltro:int, sigma:float):


   
    b,g,r = cv2.split(img_cv)
     
    linhasMatrizImagem, colunasMatrizImagem = r.shape 
 
    #tamanho acho que só pode ser ímpar, relembrar
    #criar fórmula do gaussiano 
    #montar matriz
    #funcaoG = (1 / (2 * np.pi * (sigma ** 2))) * (np.e ** ((-1*((x ** 2) + (y ** 2))) / (2 * (sigma ** 2))))
    #acho que depois de um valor o filtro para de incrementar o blur, valores ficam iguais após divisão
    '''kernel = np.zeros(shape=(tamanhoFiltro,tamanhoFiltro))
   # print(kernel.dtype)
    soma = 0
    for x in range(0,tamanhoFiltro):
        for y in range(0, tamanhoFiltro):
            kernel[x][y] = (np.e ** ((-1*((x ** 2) + (y ** 2))) / (2 * (sigma ** 2))))
            soma += kernel[x][y]
    
    print(kernel)
    for x in range(0,tamanhoFiltro):
        for y in range(0, tamanhoFiltro):
            kernel[x][y] /= soma'''

    






    kernel = np.array([
                    [1, 6, 15, 20, 15, 6, 1],
                    [6, 36, 90, 120, 90, 36, 6],
                    [15, 90, 225, 300, 225, 90, 15],
                    [20, 120, 300, 400, 300, 120, 20],
                    [15, 90, 225, 300, 225, 90, 15],
                    [6, 36, 90, 120, 90, 36, 6],
                    [1, 6, 15, 20, 15, 6, 1]                  
                    ])
    
    ordemMatrizKernel = tamanhoFiltro
    bordas = ordemMatrizKernel // 2 #tanto faz linha ou coluna
    divisao = 4096
    #print(f'divi {divisao}')
    
    matrizZero = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)

    matrizImagemParaFiltro = matrizComBordasZeradas(b, matrizZero, bordas, matrizZero.shape)
    b = convolucao(b,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem,divisao)

    matrizImagemParaFiltro = matrizComBordasZeradas(g, matrizZero, bordas, matrizZero.shape)
    g = convolucao(g,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem, divisao)

    matrizImagemParaFiltro = matrizComBordasZeradas(r, matrizZero, bordas, matrizZero.shape)
    r = convolucao(r,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem, divisao)
    
    return cv2.merge((b, g, r))



def filtroMediana(tamanhoFiltro:int):

    b,g,r = cv2.split(img_cv)
    
    linhasMatrizImagem, colunasMatrizImagem = r.shape 
    ordemMatrizKernel = tamanhoFiltro
    bordas = ordemMatrizKernel // 2
    print(f'tam r {colunasMatrizImagem} tam b {b.shape}')
    
    matrizZeroB = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)
    matrizZeroG = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)
    matrizZeroR = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)
    tamzL,tamzA = matrizZeroB.shape 
    #-----------------------------------------------------------------------------------------------------------------------------
    
    #valores das arestas
    matrizZeroB[bordas-1][bordas - 1] = b[0][0]#legal
    matrizZeroB[(tamzL - bordas)][bordas-1] = b[linhasMatrizImagem - 1][0]#legal
    matrizZeroB[bordas-1][colunasMatrizImagem + bordas] = b[0][colunasMatrizImagem - 1]#legal
    matrizZeroB[(linhasMatrizImagem + bordas)][(colunasMatrizImagem + bordas)] = b[linhasMatrizImagem - 1][colunasMatrizImagem - 1]#legal
    #valores das arestas, aí em cima
    
    #valores das linhas entre as arestas
    #legal
    matrizZeroB[bordas - 1][bordas:tamzA - bordas] = b[0][:]
    #legal
    matrizZeroB[linhasMatrizImagem + bordas][bordas:tamzA - bordas] = b[linhasMatrizImagem - 1][:] # até aqui tá certo
    
    #legal
    #valores das linhas entre as arestas, aí em cima
    index = 0
    #valores das colunas
    for i in range(bordas,linhasMatrizImagem+bordas):     
        matrizZeroB[i][bordas - 1] = b[0][index]
        
        matrizZeroB[i][tamzA - bordas] = b[linhasMatrizImagem - 1][index]
        index += 1
        if index == colunasMatrizImagem:
            index = 0
    
    #valores das colunas, entre as arestas       
        #matrizZeroB[i][colunasMatrizImagem + 1] = b[i-1][linhasMatrizImagem - 1]
        #matrizZeroB[tamzA - bordas][i] = b[linhasMatrizImagem - 1][i-1]
    #preenche as demais colunas
    
    index = 0
    for i in range(bordas,linhasMatrizImagem+bordas):
        #print(f'i:{i} bordas:{bordas}')
        for j in range(0, bordas - 1):
            matrizZeroB[i][j] = b[0][index]
            if i == bordas:
                matrizZeroB[i - 1][j] = matrizZeroB[i - 1][bordas - 1]
                matrizZeroB[i - 1][(tamzA - bordas) + j + 1] = matrizZeroB[i - 1][(tamzA - bordas) + j]
            if i == (linhasMatrizImagem + bordas) - 1:
                matrizZeroB[linhasMatrizImagem + bordas][j] = matrizZeroB[linhasMatrizImagem + bordas][bordas - 1]
                matrizZeroB[linhasMatrizImagem + bordas][(tamzA - bordas) + j + 1] = b[linhasMatrizImagem - 1][index]
            #matrizZeroB[i][j] = matrizZeroB[i][bordas - 1]
            matrizZeroB[i][(tamzA - bordas) + j + 1] = b[linhasMatrizImagem - 1][index]
       
        index += 1
        if index == colunasMatrizImagem:
            index = 0
    
    #preenche as demais colunas, aí em cima
    index = 1
    while index < bordas:
        matrizZeroB[:index][:] = matrizZeroB[bordas - 1][:]
        matrizZeroB[(linhasMatrizImagem + bordas + index)][:] = matrizZeroB[linhasMatrizImagem + bordas][:]
        
        index += 1
    
    #PARA b FOI AÍ EM CIMA
     #valores das arestas
    matrizZeroR[bordas-1][bordas - 1] = r[0][0]#legal
    matrizZeroR[(tamzL - bordas)][bordas-1] = r[linhasMatrizImagem - 1][0]#legal
    matrizZeroR[bordas-1][colunasMatrizImagem + bordas] = r[0][colunasMatrizImagem - 1]#legal
    matrizZeroR[(linhasMatrizImagem + bordas)][(colunasMatrizImagem + bordas)] = r[linhasMatrizImagem - 1][colunasMatrizImagem - 1]#legal
    #valores das arestas, aí em cima
    
    #valores das linhas entre as arestas
    #legal
    matrizZeroR[bordas - 1][bordas:tamzA - bordas] = r[0][:]
    #legal
    matrizZeroR[linhasMatrizImagem + bordas][bordas:tamzA - bordas] = r[linhasMatrizImagem - 1][:]
    #legal
    #valores das linhas entre as arestas, aí em cima
    index = 0
    #valores das colunas
    for i in range(bordas,linhasMatrizImagem+bordas):      
        matrizZeroR[i][bordas - 1] = r[0][index]
        matrizZeroR[i][tamzA - bordas] = r[linhasMatrizImagem - 1][index]
        index += 1
        if index == colunasMatrizImagem:
            index = 0
    
    index = 0
    for i in range(bordas,linhasMatrizImagem+bordas):
        #print(f'i:{i} bordas:{bordas}')
        for j in range(0, bordas - 1):
            matrizZeroR[i][j] = b[0][index]
            if i == bordas:
                matrizZeroR[i - 1][j] = matrizZeroR[i - 1][bordas - 1]
                matrizZeroR[i - 1][(tamzA - bordas) + j + 1] = matrizZeroR[i - 1][(tamzA - bordas) + j]
            if i == (linhasMatrizImagem + bordas) - 1:
                matrizZeroR[linhasMatrizImagem + bordas][j] = matrizZeroR[linhasMatrizImagem + bordas][bordas - 1]
                matrizZeroR[linhasMatrizImagem + bordas][(tamzA - bordas) + j + 1] = r[linhasMatrizImagem - 1][index]
            #matrizZeroB[i][j] = matrizZeroB[i][bordas - 1]
            matrizZeroR[i][(tamzA - bordas) + j + 1] = r[linhasMatrizImagem - 1][index]
       
        index += 1
        if index == colunasMatrizImagem:
            index = 0
    
    #preenche as demais colunas, aí em cima
    index = 1
    while index < bordas:
        matrizZeroR[:index][:] = matrizZeroR[bordas - 1][:]
        matrizZeroR[(linhasMatrizImagem + bordas + index)][:] = matrizZeroR[linhasMatrizImagem + bordas][:]
        
        index += 1
    #PARA R FOI AÍ EM CIMA
     #valores das arestas
    matrizZeroG[bordas-1][bordas - 1] = g[0][0]#legal
    matrizZeroG[(tamzL - bordas)][bordas-1] = g[linhasMatrizImagem - 1][0]#legal
    matrizZeroG[bordas-1][colunasMatrizImagem + bordas] = g[0][colunasMatrizImagem - 1]#legal
    matrizZeroG[(linhasMatrizImagem + bordas)][(colunasMatrizImagem + bordas)] = g[linhasMatrizImagem - 1][colunasMatrizImagem - 1]#legal
    #valores das arestas, aí em cima
    
    #valores das linhas entre as arestas
    #legal
    matrizZeroG[bordas - 1][bordas:tamzA - bordas] = g[0][:]
    #legal
    matrizZeroG[linhasMatrizImagem + bordas][bordas:tamzA - bordas] = g[linhasMatrizImagem - 1][:]
    #legal
    #valores das linhas entre as arestas, aí em cima
    index = 0
    #valores das colunas
    for i in range(bordas,linhasMatrizImagem+bordas):      
        matrizZeroG[i][bordas - 1] = g[0][index]
        matrizZeroG[i][tamzA - bordas] = g[linhasMatrizImagem - 1][index]
        index += 1
        if index == colunasMatrizImagem:
            index = 0
    #valores das colunas, entre as arestas       
        #matrizZeroB[i][colunasMatrizImagem + 1] = b[i-1][linhasMatrizImagem - 1]
        #matrizZeroB[tamzA - bordas][i] = b[linhasMatrizImagem - 1][i-1]
    #preenche as demais colunas
    
    index = 0
    for i in range(bordas,linhasMatrizImagem+bordas):
        #print(f'i:{i} bordas:{bordas}')
        for j in range(0, bordas - 1):
            matrizZeroG[i][j] = g[0][index]
            if i == bordas:
                matrizZeroG[i - 1][j] = matrizZeroG[i - 1][bordas - 1]
                matrizZeroG[i - 1][(tamzA - bordas) + j + 1] = matrizZeroG[i - 1][(tamzA - bordas) + j]
            if i == (linhasMatrizImagem + bordas) - 1:
                
                matrizZeroG[linhasMatrizImagem + bordas][j] = matrizZeroG[linhasMatrizImagem + bordas][bordas - 1]
                matrizZeroG[linhasMatrizImagem + bordas][(tamzA - bordas) + j + 1] = g[linhasMatrizImagem - 1][index]
            #matrizZeroB[i][j] = matrizZeroB[i][bordas - 1]
            matrizZeroG[i][(tamzA - bordas) + j + 1] = g[linhasMatrizImagem - 1][index]
       
        index += 1
        if index == colunasMatrizImagem:
            index = 0
    
    #preenche as demais colunas, aí em cima
    index = 1
    while index < bordas:
        matrizZeroG[:index][:] = matrizZeroG[bordas - 1][:]
        matrizZeroG[(linhasMatrizImagem + bordas + index)][:] = matrizZeroG[linhasMatrizImagem + bordas][:]
        
        index += 1
    #PARA G FOI AÍ EM CIMA
    #---------------------------------------------------------------------------------------------------------
    matrizZeroB = matrizComBordasZeradas(b, matrizZeroB, bordas, matrizZeroB.shape)
    matrizZeroG = matrizComBordasZeradas(g, matrizZeroG, bordas, matrizZeroG.shape)
    matrizZeroR = matrizComBordasZeradas(r, matrizZeroR, bordas, matrizZeroR.shape)

    
    matrizMediana = np.zeros(shape=(tamanhoFiltro * tamanhoFiltro)).astype(int)
    #print(f'tamanho matriz mediana {matrizMediana}')
    for i in range(0, linhasMatrizImagem):
        z = 0
        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            
            soma = 0
            ind = 0
            for p in range(0,ordemMatrizKernel):
                z = j
                
                for v in range(0,ordemMatrizKernel):
                    #print(f'indi {ind} | p {p} r {r}')
                    matrizMediana[ind] = matrizZeroB[x][z]
                    ind += 1                
                    z += 1
                   # print(matrizImagemParaFiltroB[x][z], end=' ')
            
                x += 1
               # print()
            matrizMediana = np.sort(matrizMediana, kind= 'mergesort')
            #print(f'matrizMediana tem valores {matrizMediana}')
            mediana = np.median(matrizMediana).astype(int)
           # print(f'a mediana é {mediana} {i}{j}')
            b[i][j] = mediana
            #exit()
    for i in range(0, linhasMatrizImagem):
        z = 0
        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            
            soma = 0
            ind = 0
            for p in range(0,ordemMatrizKernel):
                z = j
               
                for v in range(0,ordemMatrizKernel):
                    matrizMediana[ind] = matrizZeroG[x][z]
                    ind += 1                
                    z += 1
            
                x += 1
            matrizMediana = np.sort(matrizMediana, kind= 'mergesort')
            mediana = np.median(matrizMediana).astype(int)
            g[i][j] = mediana
    
    for i in range(0, linhasMatrizImagem):
        z = 0
        for j in range(0, colunasMatrizImagem):
            x = i
            z = j
            
            soma = 0
            ind = 0
            for p in range(0,ordemMatrizKernel):
                z = j
               
                for v in range(0,ordemMatrizKernel):
                    matrizMediana[ind] = matrizZeroR[x][z]
                    ind += 1                
                    z += 1
            
                x += 1
            matrizMediana = np.sort(matrizMediana, kind= 'mergesort')
            mediana = np.median(matrizMediana).astype(int)
            
            r[i][j] = mediana
           # print(f'medina {mediana} i {i}')
    return cv2.merge((b, g, r))


def apply_filter(filter_type):
    #print(f'tamanho da matriz: {img_cv.shape}')
    if img_cv is None:
        return
    
    if filter_type == "low_pass":
       
        filtered_img = filtroGaussiano(7,50)
        
       
        #filtered_img = img_cv
        #print(img_cv.shape)
        #print(filtered_img)
       
        #filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)
        #filtered_img = cv2.GaussianBlur(img_cv, (15, 15), 0)
    elif filter_type == "high_pass":
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        filtered_img = cv2.Laplacian(gray, cv2.CV_64F)
        filtered_img = cv2.convertScaleAbs(filtered_img)
        filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)
    display_image(filtered_img, original=False)  # Exibe a imagem editada

def refresh_canvas():
    edited_image_canvas.delete("all")  # Limpa a canvas para exibir a nova imagem

# Definindo a GUI
root = tk.Tk()
root.title("Image Processing App")

# Define o tamanho da janela da aplicação 1200x800
root.geometry("1085x550")

# Define a cor de fundo da janela
root.config(bg="#2e2e2e")

img_cv = None

# Cria o menu da aplicação
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Load Image", command=load_image)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Filters menu
filters_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Filters", menu=filters_menu)
filters_menu.add_command(label="Low Pass Filter", command=lambda: apply_filter("low_pass"))
filters_menu.add_command(label="High Pass Filter", command=lambda: apply_filter("high_pass"))

# Cria a canvas para a imagem original com borda (sem background)
original_image_canvas = tk.Canvas(root, width=500, height=500, bg="#2e2e2e", highlightthickness=1, highlightbackground="white")
original_image_canvas.grid(row=0, column=0, padx=20, pady=20)

# Cria a canvas para a imagem editada com borda (sem background)
edited_image_canvas = tk.Canvas(root, width=500, height=500, bg="#2e2e2e", highlightthickness=1, highlightbackground="white")
edited_image_canvas.grid(row=0, column=1, padx=20, pady=20)

root.mainloop()
