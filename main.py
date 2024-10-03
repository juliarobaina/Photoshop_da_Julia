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
                    
                    z += 1
               
                x += 1
            
            pixelNovo = abs(floor(soma / divisor)) #abs é para o sobel, talvez todos passa-alta
           
            if pixelNovo > 255: #normalização, pixels variam de 0-255
                filtered_img[i][j] = 255
            else:
                filtered_img[i][j] = pixelNovo
           
    
    return filtered_img

def filtroMedia(tamanhoKernel:int):#blur
    
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
   
    #sigma:float é parâmetro da função
    #tamanho acho que só pode ser ímpar, relembrar
    #criar fórmula do gaussiano 
    #montar matriz
    #funcaoG = (1 / (2 * np.pi * (sigma ** 2))) * (np.e ** ((-1*((x ** 2) + (y ** 2))) / (2 * (sigma ** 2))))
    #depois de um valor o filtro para de incrementar o blur, valores ficam iguais após divisão. É porque os valores ficam muito pequenos e o floor arredonda tudo pro mesmo número. Mesmo não usando floor as diferenças são tão pequenas que são imperceptíveis
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

    
    kernel, divisor = kernelGaussiano(tamanhoKernel)
    
    bordas = tamanhoKernel // 2
   
    #matrizZero = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)

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
    #valores das arestas, aí em cima
    
    #valores das linhas entre as arestas
    matrizParaMediana[bordas - 1][bordas:tamzA - bordas] = matriz[0][:]
    matrizParaMediana[linhasMatrizImagem + bordas][bordas:tamzA - bordas] = matriz[linhasMatrizImagem - 1][:]
  
    #valores das linhas entre as arestas, aí em cima

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
    
    #preenche as demais colunas, aí em cima
    index = 1
    while index < bordas:
        matrizParaMediana[:index][:] = matrizParaMediana[bordas - 1][:]
        matrizParaMediana[(linhasMatrizImagem + bordas + index)][:] = matrizParaMediana[linhasMatrizImagem + bordas][:]

        index += 1

    return matrizParaMediana

def convolucaoMediana(matriz, matrizBordasGemeas, tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem):
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

  
    convolucaoMediana(b,matrizComBordasGemeasB,tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem)
    convolucaoMediana(g,matrizComBordasGemeasG,tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem)
    convolucaoMediana(r,matrizComBordasGemeasR,tamanhoKernel, linhasMatrizImagem, colunasMatrizImagem)
   
    return cv2.merge((b, g, r))


def kernelSobel():
    
    kernelHorizontal = [[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]
                    ]
    kernelVertical = [[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]
                    ]
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
        kernel = [[1, 2, 1],
                  [2, 4, 2],
                  [1, 2, 1]]
        divisor = 16

    elif tamanho == 5:
        kernel = [[1, 4, 7, 4, 1],
                  [4, 16, 26, 16, 4],
                  [7, 26, 41, 26, 7],
                  [4, 16, 26, 16, 4],
                  [1, 4, 7, 4, 1]
                ]
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

    matrizCinza = cv2.cvtColor(imgGaussiano, cv2.COLOR_BGR2GRAY)
    
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

    matrizCinza = cv2.cvtColor(imgGaussiano, cv2.COLOR_BGR2GRAY)
    
    linhasMatrizImagem, colunasMatrizImagem = matrizCinza.shape 
    
    kernel = kernelLaplaciano()
   
    ordemMatrizKernel = 3
    bordas = ordemMatrizKernel // 2
  
   
    divisao = 1
   
    matrizImagemParaFiltro = matrizComBordasZeradas(matrizCinza, bordas, linhasMatrizImagem, colunasMatrizImagem)
    b = convolucao(matrizCinza,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem,divisao)
    
    return b
    
def apply_filter(filter_type):
    #print(f'tamanho da matriz: {img_cv.shape}')
    if img_cv is None:
        return
    
    if filter_type == "low_pass":

    
        filtered_img = filtroLaplaciano()
        
       
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

#menu com 2 níveis
'''filters_menu2 = tk.Menu(menu_bar, tearoff=0)
filters_menu3.add_cascade(label="Filters 2", menu=filters_menu2)
filters_menu3 = tk.Menu(filters_menu3, tearoff=0)
filters_menu3.add_cascade(label="Filtro Passa-Baixa", menu=filters_menu3)
filters_menu3.add_cascade(label="Média", command=lambda: apply_filter("low_pass"))
filters_menu3.add_command(label="3 x 3", command=load_image)'''

# Cria a canvas para a imagem original com borda (sem background)
original_image_canvas = tk.Canvas(root, width=500, height=500, bg="#2e2e2e", highlightthickness=1, highlightbackground="white")
original_image_canvas.grid(row=0, column=0, padx=20, pady=20)

# Cria a canvas para a imagem editada com borda (sem background)
edited_image_canvas = tk.Canvas(root, width=500, height=500, bg="#2e2e2e", highlightthickness=1, highlightbackground="white")
edited_image_canvas.grid(row=0, column=1, padx=20, pady=20)

root.mainloop()
