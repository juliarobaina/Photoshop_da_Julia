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
submenu_limiar_label = None
btnSimples = None
btnOtsu = None
btnMedia = None
btnBernsen = None
clique = 1
tipo2State = 'Fechado'

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
        case 'PA':
            nomeImagemTop = 'hoverTopPA.png'
            nomeImagemBottom = 'hoverBottomPA.png'
        case 'SG':
            nomeImagemTop = 'hoverTopSG.png'
            nomeImagemBottom = 'hoverBottomSG.png'
        
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


def LG():
    global btnSimples, btnOtsu, btnMedia, btnBernsen
    
    btnSimples = ctk.CTkButton(janela,text='Simples',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Global Simples'))
    btnSimples.place(x=231,y = 442)#

    #Para aplicar o efeito de hover
    btnSimples.bind("<Enter>", command=lambda event: hover(231,442,'SG'))
    btnSimples.bind("<Leave>", command=leave)

    btnOtsu = ctk.CTkButton(janela,text='Otsu',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Global Otsu'))
    btnOtsu.place(x=231,y = 472)#
    
    #Para aplicar o efeito de hover
    btnOtsu.bind("<Enter>", command=lambda event: hover(231,472,'SG'))
    btnOtsu.bind("<Leave>", command=leave)

def LA():
    global btnSimples, btnOtsu, btnMedia, btnBernsen
    
    btnMedia = ctk.CTkButton(janela,text='Média',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Media'))
    btnMedia.place(x=231,y = 442)#

    #Para aplicar o efeito de hover
    btnMedia.bind("<Enter>", command=lambda event: hover(231,442,'SG'))
    btnMedia.bind("<Leave>", command=leave)

    btnOtsu = ctk.CTkButton(janela,text='Otsu',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Otsu'))
    btnOtsu.place(x=231,y = 472)#
    
    #Para aplicar o efeito de hover
    btnOtsu.bind("<Enter>", command=lambda event: hover(231,472,'SG'))
    btnOtsu.bind("<Leave>", command=leave)

    btnBernsen = ctk.CTkButton(janela,text='Bernsen',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Bernsen'))
    btnBernsen.place(x=231,y = 502)#
    
    #Para aplicar o efeito de hover
    btnBernsen.bind("<Enter>", command=lambda event: hover(231,502,'SG'))
    btnBernsen.bind("<Leave>", command=leave)

def abrirfecharJanelaLimiar(tipo, tipo2):
    global clique
    global submenu_limiar_label
    
    global tipo2State
   
    print(f'vv {clique}')
    if clique % 2 == 0 and tipo2State != "Fechado":
        print(f'clique {clique}')
        print(f'tipo2S {tipo2State} {tipo2}')
        if tipo2 == 'fecharLA' and tipo2State == tipo2:
            tipo2State = 'Fechado'
            
            submenu_limiar_label.destroy()
            btnOtsu.destroy()
            btnMedia.destroy()
            btnBernsen.destroy()
           
        elif tipo2 == 'fecharLA' and tipo2State != tipo2:
            tipo2State = tipo2

            print('faz aí alguma coisa?1')
            btnSimples.destroy()
            btnOtsu.destroy()
            LA()
        elif tipo2 == 'fecharLG' and tipo2State != tipo2:
            tipo2State = tipo2
            print('faz aí alguma coisa?2')
            btnOtsu.destroy()
            btnMedia.destroy()
            btnBernsen.destroy()
            LG()
        elif tipo2 == 'fecharLG':
            tipo2State = 'Fechado'
            submenu_limiar_label.destroy()
            btnSimples.destroy()
            btnOtsu.destroy()
    
    elif clique % 2 != 0 and tipo2State != "Fechado":
        if tipo2 == 'fecharLA' and tipo2State == tipo2:
            tipo2State = 'Fechado'
            
            submenu_limiar_label.destroy()
            btnOtsu.destroy()
            btnMedia.destroy()
            btnBernsen.destroy()
           
        elif tipo2 == 'fecharLA' and tipo2State != tipo2:
            tipo2State = tipo2

            print('faz aí alguma coisa?1')
            btnSimples.destroy()
            btnOtsu.destroy()
            LA()
        elif tipo2 == 'fecharLG' and tipo2State != tipo2:
            tipo2State = tipo2
            print('faz aí alguma coisa?2')
            btnOtsu.destroy()
            btnMedia.destroy()
            btnBernsen.destroy()
            LG()
        elif tipo2 == 'fecharLG':
            tipo2State = 'Fechado'
            submenu_limiar_label.destroy()
            btnSimples.destroy()
            btnOtsu.destroy()
    

    else:
        tipo2State = tipo2
        submenu_limiar_label = ctk.CTkLabel(frameEsquerdo,width=220, height=100,bg_color="#1c1c1c", fg_color="#1c1c1c", text='', font=fontC, text_color="#848484",anchor='nw', padx=10,pady=10)
        submenu_limiar_label.place(x=220, y=432)
        clique += 1
        if tipo == 'LG': 
            LG()
            ''' btnSimples = ctk.CTkButton(janela,text='Simples',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Global Simples'))
            btnSimples.place(x=231,y = 442)#

            #Para aplicar o efeito de hover
            btnSimples.bind("<Enter>", command=lambda event: hover(231,442,'SG'))
            btnSimples.bind("<Leave>", command=leave)

            btnOtsu = ctk.CTkButton(janela,text='Otsu',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Global Otsu'))
            btnOtsu.place(x=231,y = 472)#
            
            #Para aplicar o efeito de hover
            btnOtsu.bind("<Enter>", command=lambda event: hover(231,472,'SG'))
            btnOtsu.bind("<Leave>", command=leave)'''
        
        elif tipo == 'LA':
            LA()
            '''btnMedia = ctk.CTkButton(janela,text='Média',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Media'))
            btnMedia.place(x=231,y = 442)#

            #Para aplicar o efeito de hover
            btnMedia.bind("<Enter>", command=lambda event: hover(231,442,'SG'))
            btnMedia.bind("<Leave>", command=leave)

            btnOtsu = ctk.CTkButton(janela,text='Otsu',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Otsu'))
            btnOtsu.place(x=231,y = 472)#
            
            #Para aplicar o efeito de hover
            btnOtsu.bind("<Enter>", command=lambda event: hover(231,472,'SG'))
            btnOtsu.bind("<Leave>", command=leave)

            btnBernsen = ctk.CTkButton(janela,text='Bernsen',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Bernsen'))
            btnBernsen.place(x=231,y = 502)#
            
            #Para aplicar o efeito de hover
            btnBernsen.bind("<Enter>", command=lambda event: hover(231,502,'SG'))
            btnBernsen.bind("<Leave>", command=leave)'''
    
            
   

   # btnLimiarG = ctk.CTkButton(janela,text="Simples",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc("Limiar Global Simples"))
   # btnLimiarG.place(x=230,y=472)#
    


# Cria a canvas para a imagem original com borda (sem background)
original_image_canvas = ctk.CTkCanvas(janela, width=700, height=700, bg="#171717",  highlightthickness=0)
original_image_canvas.place(x=320,y=150)

# Cria a canvas para a imagem editada com borda (sem background)
edited_image_canvas = ctk.CTkCanvas(janela, width=700, height=700, bg="#171717", highlightthickness=0)
edited_image_canvas.place(x=1060,y=150)

#fonte dos menus
fontD = ctk.CTkFont(family="Inconsolata",size=14)
#fonte do menu geral
fontB = ctk.CTkFont(family="Inconsolata",size=14)
#Fonte de título de cada seção
fontC = ctk.CTkFont(family="Inconsolata",size=13, weight="bold")


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


btnCarregarImagem = ctk.CTkButton(janela,text="Carregar Imagem",image=carregarImagem, bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=load_image, font=fontB, hover=False)

btnCarregarImagem.place(x=10,y=65)
btnCarregarImagem.configure(cursor="hand2")
btnSalvarImagem = ctk.CTkButton(janela,text="Salvar Imagem",image=salvarImagem,bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontB,hover=False).place(x=10,y=105)
#separador de seção
separador = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  size=(220, 2))
separador_label = ctk.CTkLabel(frameEsquerdo, image=separador, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",height=2).place(x=0,y=145)  




'''Menu Passa-Baixa'''
#bullets points
marcadorPB = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/marcadorPassaBaixa.png"),
                                  size=(8, 8))

btnGaussiano = ctk.CTkButton(janela,text="Gaussiano",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Gaussiano"), font=fontD,hover=False,image=marcadorPB)
btnGaussiano.place(x=12,y=181)
#Para aplicar o efeito de hover
btnGaussiano.bind("<Enter>", command=lambda event: hover(12,181,'PB'))
btnGaussiano.bind("<Leave>", command=leave)

btnMedia = ctk.CTkButton(janela,text="Média",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Media"), font=fontD, image=marcadorPB, hover=False)
btnMedia.place(x=12,y=211)

#Para aplicar o efeito de hover
btnMedia.bind("<Enter>", command=lambda event: hover(12,211,'PB'))
btnMedia.bind("<Leave>", command=leave)

btnMediana = ctk.CTkButton(janela,text="Mediana",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Mediana"), font=fontD, image=marcadorPB, hover=False)
btnMediana.place(x=12,y=241)

#Para aplicar o efeito de hover
btnMediana.bind("<Enter>", command=lambda event: hover(12,241,'PB'))
btnMediana.bind("<Leave>", command=leave)

#separador de seção
separador = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  size=(220, 2))
separador_label = ctk.CTkLabel(frameEsquerdo, image=separador, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",height=2).place(x=0,y=271)  

'''Menu Passa-Alta'''
#bullets points
marcadorPA = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/marcadorPassaAlta.png"),
                                  size=(8, 8))

btnSobel = ctk.CTkButton(janela,text="Sobel",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Sobel"), font=fontD,hover=False,image=marcadorPA)
btnSobel.place(x=12,y=306)
#Para aplicar o efeito de hover
btnSobel.bind("<Enter>", command=lambda event: hover(12,306,'PA'))
btnSobel.bind("<Leave>", command=leave)

btnLaplaciano = ctk.CTkButton(janela,text="Laplaciano",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Laplaciano"), font=fontD, image=marcadorPA, hover=False)
btnLaplaciano.place(x=12,y=336)

#Para aplicar o efeito de hover
btnLaplaciano.bind("<Enter>", command=lambda event: hover(12,336,'PA'))
btnLaplaciano.bind("<Leave>", command=leave)


#separador de seção
separador = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  size=(220, 2))
separador_label = ctk.CTkLabel(frameEsquerdo, image=separador, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",height=2).place(x=0,y=366)  

'''Menu Segmentação'''
#bullets points
marcadorSG = ctk.CTkImage(Image.open("C:/Users/julia/Downloads/marcadorSegmentacao.png"), size=(8, 8))
btnBinarizacao = ctk.CTkButton(janela,text="Binarização",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Binarizacao"), font=fontD, image=marcadorSG, hover=False)
btnBinarizacao.place(x=12,y=402)

#Para aplicar o efeito de hover
btnBinarizacao.bind("<Enter>", command=lambda event: hover(12,402,'SG'))
btnBinarizacao.bind("<Leave>", command=leave)

btnLimiarG = ctk.CTkButton(janela,text="Limiarização Global",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False)
btnLimiarG.place(x=12,y=432)#command=lambda:setFuncaoEsc("Limiar Global")
setaDir = ctk.CTkImage(Image.open("C:/Users/julia/Downloads/setaDireita.png"), size=(24, 24))
setaDir_label = ctk.CTkLabel(frameEsquerdo,width=0, height=0,bg_color="#1c1c1c", fg_color="#1c1c1c",image=setaDir, text='')
setaDir_label.place(x=160, y=431.5)
setaDir_label = ctk.CTkLabel(frameEsquerdo,width=0, height=0,bg_color="#1c1c1c", fg_color="#1c1c1c",image=setaDir, text='')
setaDir_label.place(x=185, y=463)
#Para aplicar o efeito de hover
btnLimiarG.bind("<Enter>", command=lambda event: hover(12,432,'SG'))
btnLimiarG.bind("<Leave>", command=leave)

btnLimiarA = ctk.CTkButton(janela,text="Limiarização Adaptativa",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False)
btnLimiarA.place(x=12,y=462)#command=lambda:setFuncaoEsc("Limiar Adaptativo")

#Para aplicar o efeito de hover
btnLimiarA.bind("<Enter>", command=lambda event: hover(12,462,'SG'))
btnLimiarA.bind("<Leave>", command=leave)

#submenu limiarização global
btnLimiarG.bind("<Button-1>", command=lambda event: abrirfecharJanelaLimiar('LG', 'fecharLG'))

btnLimiarA.bind("<Button-1>", command=lambda event: abrirfecharJanelaLimiar('LA', 'fecharLA'))

#btnLimiarA.bind("<ButtonRelease-1>", command=lambda event: fecharJanelaLimiar('LA'))


'''Menu Morfologia'''
#btnErosao = ctk.CTkButton(janela,text="Erosão",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Erosao")).place(x=12,y=260)



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


labelPB = ctk.CTkLabel(frameEsquerdo,text="Filtros Passa-Baixa",bg_color="#1c1c1c",fg_color="#1c1c1c",text_color="#848484", font=fontC).place(x=10,y=155)

labelPA = ctk.CTkLabel(frameEsquerdo,text="Filtros Passa-Alta",bg_color="#1c1c1c",fg_color="#1c1c1c",text_color="#848484", font=fontC).place(x=10,y=281)

labelSeg = ctk.CTkLabel(frameEsquerdo,text="Segmentação",bg_color="#1c1c1c",fg_color="#1c1c1c",text_color="#848484", font=fontC).place(x=10,y=376)



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

