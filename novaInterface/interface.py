import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from funcoesProcessamentoImagem import filtroGaussiano,erosao,binarizacao, escalaDeCinza

FUNCAOESC = 'vazio'
VALORJANELA = 3
VALORLIMIAR = 3
img_cv = None
img_pil = None
cambalacho = 1
hoverTop = None
hoverBottom = None
hoverTop_label = None
hoverBottom_label = None


'''Criar a janela principal'''
janela = ctk.CTk() 


'''configurar a janela principal'''
janela.geometry("1445x760")
janela.title("Photoshop da Julia")
janela.config(bg="#141414")

'''funções de interação com a interface e comunicação com o back-end'''
def setValorJanela(value):
    my_label.configure(text=int(value))
    global VALORJANELA 
    VALORJANELA = int(value)

def setValorLimiar(value):
    my_labelLimiar.configure(text=int(value))
    global VALORLIMIAR 
    VALORLIMIAR = int(value)

def a(val):
    print(val)
    global img_cv
    match(FUNCAOESC):
        case 'Gaussiano':
            print(f'a função é gaussiano e com valor de janela {VALORJANELA}')
            filtered_img = filtroGaussiano(VALORJANELA, img_cv)
            
            img_cv=filtered_img
            print('-----------------------')
            print(img_cv)
        case 'Media':
            print(f'a função é média e com valor de janela {VALORJANELA}')
        
        case 'Erosao':
           # filtered_img = erosao(img_cv, VALORJANELA)
            
            #img_cv=filtered_img
            pass
        case 'Binarizacao':
           ''' filtered_img = escalaDeCinza(img_cv)
            filtered_img = binarizacao(VALORLIMIAR, filtered_img)
            img_cv=filtered_img'''
           pass
        case 'vazio':
            print(f'escolha uma função primeiro')
    display_image(filtered_img, original=False)  # Exibe a imagem editada


def setFuncaoEsc(esc):
    global FUNCAOESC
    global img_cv
    FUNCAOESC = esc
    filtered_img = img_cv
    global cambalacho
    if FUNCAOESC == 'Gaussiano' or FUNCAOESC == 'Media':
        #number_of_steps=126 tem que fazer conta tipo como é de 3 a 255, fica (255 -3) / 126 pro slide pular de 2 em 2
        slider.configure(state="normal", number_of_steps=126)#desbloqueia slide após escolher uma opção, fazer personalizado
        filtered_img = filtroGaussiano(VALORJANELA, img_cv)
            
        img_cv=filtered_img
        # Exibe a imagem editada
    elif FUNCAOESC == 'Erosao':
       # 
        filtered_img = erosao(img_cv, VALORJANELA)
            
        img_cv=filtered_img
    elif FUNCAOESC == 'Binarizacao':
        #sliderLimiar.configure(state="normal")
        print(f'limiar = {VALORLIMIAR}')
        print(img_cv)
        if cambalacho == 1:
            filtered_img = escalaDeCinza(img_cv)
            cambalacho = 2
        print(f'cambalacho {cambalacho}')
        print(filtered_img.shape)
        filtered_img = binarizacao(VALORLIMIAR, filtered_img)
        img_cv=filtered_img
    print(FUNCAOESC)
    display_image(filtered_img, original=False) 



def load_image():
    global img_cv
   
    file_path = ctk.filedialog.askopenfile(title='Escolha uma imagem', filetypes=[("Arquivos de imagem", "*.jpeg;*.jpg;*.jfif;*.png;*.bmp;*.tif;*.tiff;*.gif;*.webp;*.pbm;*.pgm;*.ppm;*.heif;*.heic")])#verificar extensões depois
    if file_path:
        print(file_path)
        img_cv = cv2.imread(file_path.name)
        display_image(img_cv, original=True)  # Exibe a imagem original
        refresh_canvas()

def display_image(img, original=False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    global img_pil
    img_pil = Image.fromarray(img_rgb)
    
    # Obtém o tamanho da imagem original
   # img_width, img_height = img_pil.size
    
    # Redimensional a imagem para caber no canvas se for muito grande
    max_size = 700
    img_pil.thumbnail((max_size, max_size))  # Maintain aspect ratio
    img_tk = ImageTk.PhotoImage(img_pil)

    # Calcula a posição para centralizar a imagem dentro do canvas se for menor
    canvas_width, canvas_height = max_size, max_size
    x_offset = (canvas_width - img_pil.width) // 2
    y_offset = (canvas_height - img_pil.height) // 2

    if original:
        original_image_canvas.delete("all")  # Limpa a canvas
        original_image_canvas.image = img_tk  # Mantém a referência viva - garbage collection
        original_image_canvas.create_image(x_offset, y_offset, anchor=ctk.NW, image=img_tk)
    else:
        edited_image_canvas.delete("all")  # Limpa a canvas
        edited_image_canvas.image = img_tk
        edited_image_canvas.create_image(x_offset, y_offset, anchor=ctk.NW, image=img_tk)
        
def refresh_canvas():
    edited_image_canvas.delete("all")  # Limpa a canvas para exibir a nova imagem


def hover(xF, yF, tipo):
    global hoverBottom_label, hoverTop_label
    nomeImagemTop = ''
    nomeImagemBottom = ''
    pathImagem = "C:/Users/julia/Downloads/"
    match tipo:
        case 'PB':
            nomeImagemTop = 'hoverTopPB.png'
            nomeImagemBottom = 'hoverBottomPB.png'
    hoverTop = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemTop),
                                  size=(180, 3))
    # display image with a CTkLabel
    hoverTop_label = ctk.CTkLabel(frameEsquerdo, image=hoverTop, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverTop_label.place(x=xF + 16,y= yF + 1) 
    
    hoverBottom = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemBottom),
                                  size=(180, 3))
    
    # display image with a CTkLabel
    hoverBottom_label = ctk.CTkLabel(frameEsquerdo, image=hoverBottom, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverBottom_label.place(x=xF + 16,y=yF + 19) 

def leave(v):
    hoverTop_label.destroy()
    hoverBottom_label.destroy()

# Cria a canvas para a imagem original com borda (sem background)
original_image_canvas = ctk.CTkCanvas(janela, width=700, height=700, bg="#171717",  highlightthickness=0)
original_image_canvas.place(x=320,y=150)

# Cria a canvas para a imagem editada com borda (sem background)
edited_image_canvas = ctk.CTkCanvas(janela, width=700, height=700, bg="#171717", highlightthickness=0)
edited_image_canvas.place(x=1060,y=150)


'''criar frames'''
frameEsquerdo = ctk.CTkFrame(master=janela,width=220,height=1000,fg_color="#1c1c1c", bg_color="#1c1c1c").place(x=0,y=0)
frameDireito = ctk.CTkFrame(master=janela, width=500,height=300, fg_color="#1c1c1c", bg_color="#1c1c1c").place(x=1050,y=50)
#frameImgOriginal = ctk.CTkFrame(master=janela, width=500,height=500, fg_color="#171717", bg_color="#171717").place(x=250,y=150)
#frameImgModificada = ctk.CTkFrame(master=janela, width=500,height=500, fg_color="#171717", bg_color="#171717").place(x=760,y=150)

'''Menu Geral'''
#logo
logo = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/logoPSJ.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/logoPSJ.png"),
                                  size=(190, 33))
# display image with a CTkLabel
logo_label = ctk.CTkLabel(frameEsquerdo, image=logo, text="",bg_color="#1c1c1c",fg_color="#1c1c1c").place(x=10,y=10)  

#Ícones do Botão
carregarImagem = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/add_photo_alternate_24dp.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/add_photo_alternate_24dp.png"),
                                  size=(24, 24))
salvarImagem = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/file_download_24dp.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/file_download_24dp.png"),
                                  size=(24, 24))

#fonte do menu geral
fontB = ctk.CTkFont(family="Inconsolata",size=15)

btnCarregarImagem = ctk.CTkButton(janela,text="Carregar Imagem",image=carregarImagem, bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=load_image, font=fontB, hover_color="#101010")

btnCarregarImagem.place(x=10,y=65)
btnCarregarImagem.configure(cursor="hand2")
btnSalvarImagem = ctk.CTkButton(janela,text="Salvar Imagem",image=salvarImagem,bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontB,hover=False).place(x=10,y=105)
#separador de seção
separador = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  size=(220, 2))
separador_label = ctk.CTkLabel(frameEsquerdo, image=separador, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",height=2).place(x=0,y=145)  




'''Menu Passa-Baixa'''
#fonte dos menus
fontD = ctk.CTkFont(family="Inconsolata",size=14)
#bullets points
marcadorPB = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/marcadorPassaBaixa.png"),
                                  size=(8, 8))

btnGaussiano = ctk.CTkButton(janela,text="Gaussiano",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Gaussiano"), font=fontD,hover=False,image=marcadorPB)
btnGaussiano.place(x=12,y=180)
#Para aplicar o efeito de hover
btnGaussiano.bind("<Enter>", command=lambda event: hover(12,180,'PB'))
btnGaussiano.bind("<Leave>", command=leave)

btnMedia = ctk.CTkButton(janela,text="Média",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Media"), font=fontD, image=marcadorPB, hover=False)
btnMedia.place(x=12,y=210)
print(abs(4-len('media')))
#Para aplicar o efeito de hover
btnMedia.bind("<Enter>", command=lambda event: hover(12,210,'PB'))
btnMedia.bind("<Leave>", command=leave)



'''Menu Segmentação'''
btnBinarizacao = ctk.CTkButton(janela,text="Binarização",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Binarizacao")).place(x=12,y=240)

'''Menu Morfologia'''
btnErosao = ctk.CTkButton(janela,text="Erosão",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Erosao")).place(x=12,y=260)



'''Menu Ajustes'''
#Botão de abrir e fechar o menu
btnAjustes = ctk.CTkButton(janela,text="Ajustes",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command="").place(x=1060,y=50)
#Slider de tamanho da janela (kernel)
slider = ctk.CTkSlider(frameDireito,from_=3, to=255, width=130,height=20,button_color="#9518f5", button_hover_color="#6D08BA",progress_color="#9518f5", command=setValorJanela, state="disabled")
slider.place(x=1070,y=80)
slider.set(3)

#Label que exibe o valor atual do slide
my_label = ctk.CTkLabel(frameDireito, text=slider.get())
my_label.place(x=1100,y=100)

print(FUNCAOESC)
#Executa uma função de processamento de imagem ao soltar o mouse do slide
slider.bind("<ButtonRelease-1>",command=a)

#Slider do Limiar
sliderLimiar = ctk.CTkSlider(frameDireito,from_=0, to=255, width=130,button_color="#9518f5", button_hover_color="#6D08BA",progress_color="#9518f5", command=setValorLimiar, state="normal")
sliderLimiar.place(x=1070,y=140)
#inicia o slide na posição 0
sliderLimiar.set(0)
#Label que exibe o valor atual do slide
my_labelLimiar = ctk.CTkLabel(frameDireito, text=sliderLimiar.get())
my_labelLimiar.place(x=1100,y=160)
#Executa uma função de processamento de imagem ao soltar o mouse do slide
sliderLimiar.bind("<ButtonRelease-1>",command=a)
print(FUNCAOESC)

'''Título de cada seção'''
#Fonte de título de cada seção
fontC = ctk.CTkFont(family="Inconsolata",size=13, weight="bold")

labelTet = ctk.CTkLabel(frameEsquerdo,text="Filtros Passa-Baixa",bg_color="#1c1c1c",fg_color="#1c1c1c",text_color="#848484", font=fontC).place(x=10,y=155)



'''
Comentários Gerais
#number_of_steps = 10 vai de 10 em 10

#janela.maxsize() pode redimensionar até tanto de tamanho
#janela.resizable() permite ou proibe redimensionar

#POP-UP
#janela = ctk.CTkToplevel(janela, fg_color="#141414")

#janela.attributes("-fullscreen", True)
#janela.state('zoomed')
#resolucaoJanelaUsuario = str(janela.winfo_screenwidth()) + 'x' + str(janela.winfo_screenheight())

'''    








janela.mainloop() 

