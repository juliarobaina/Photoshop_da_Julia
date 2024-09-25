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




kernel = np.array([[1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1]
                  ])

linhasKernel = 7
colunasKernel = 7
ordemMatrizKernel = 7
bordas = ordemMatrizKernel // 2

def matrizComBordasZeradas(matriz, matrizZero, bordas, tamanhoMatrizZero):
    index = 0

    linhasMatrizZero = tamanhoMatrizZero[0]
    colunasMatrizZero = tamanhoMatrizZero[1]
  
    for i in range(bordas, linhasMatrizZero-bordas):
      
        matrizZero[i][bordas:colunasMatrizZero - bordas] = matriz[index]
        index += 1
    return matrizZero

def filtroConvolucao(filtered_img, matrizImagemParaFiltro, kernel, ordemKernel,linhasMatrizImagem, colunasMatrizImagem):

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
              
            pixelNovo = floor(soma / 49)
              #usar matriz original em vez de B. De acordo com 1 vídeo é a soma dividido pelo 1/9 por exemplo soma * (1/9)
            if pixelNovo > 255: #normalização, pixels variam de 0-255
                filtered_img[i][j] = 255
            else:
                filtered_img[i][j] = pixelNovo
    #print(f'dentro da função filtr \n {filtered_img}')
    return filtered_img


def apply_filter(filter_type):
    #print(f'tamanho da matriz: {img_cv.shape}')
    if img_cv is None:
        return
    
    if filter_type == "low_pass":
        #filtered_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY) #faz ficar uma matriz 2x2, mais ou menos
        b,g,r = cv2.split(img_cv)
        b_novo = np.zeros_like(b)
      
        g_novo = np.zeros_like(g)
        r_novo = np.zeros_like(r)
        
       
        tamImagem = img_cv.shape
       
        #print(tamImagem[3])
        #for i in range(0,tamImagem[0]):
            #print(img_cv[i])
            #tamM = filtered_img.shape #tamanho da matriz (m,n)
           # tam = img_cv[i].shape
        linhasMatrizImagem, colunasMatrizImagem = r_novo.shape
        
        matrizZero = np.zeros(shape=(linhasMatrizImagem+(bordas*2),colunasMatrizImagem+(bordas*2))).astype(int)
        
        matrizImagemParaFiltro = matrizComBordasZeradas(b, matrizZero, bordas, matrizZero.shape)
        b_novo = filtroConvolucao(b,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem)
        matrizImagemParaFiltro = matrizComBordasZeradas(g, matrizZero, bordas, matrizZero.shape)
        g_novo = filtroConvolucao(g,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem)
        matrizImagemParaFiltro = matrizComBordasZeradas(r, matrizZero, bordas, matrizZero.shape)
        r_novo = filtroConvolucao(r,matrizImagemParaFiltro,kernel,ordemMatrizKernel,linhasMatrizImagem,colunasMatrizImagem)
        #print(img_cv)
        filtered_img = cv2.merge((b_novo, g_novo, r_novo))
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
