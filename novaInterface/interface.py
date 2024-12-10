import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from funcoesProcessamentoImagem import *

FUNCAOESC = 'vazio'
FUNCAOESC2 = []
VALORJANELA = 3
VALORLIMIAR = 0
VALORVALORC = 0
VALORKERNEL = 3
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
sliderOnOff = 0
sliderOnOff2 = 0
sliderOnOff3 = 0
sliderOnOff4 = 0
cliquePOPUP1 = 0
cliquePOPUP2 = 0 
'''Criar a janela principal'''
janela = ctk.CTk() 


'''configurar a janela principal'''
'''largura_janela = janela.winfo_screenwidth()
altura_janela = janela.winfo_screenheight()
posicao_x = (largura_janela) // 2
posicao_y = (altura_janela) // 2
janela.geometry(f"{largura_janela}x{altura_janela}+{0}+{posicao_y}")'''
janela.geometry("1445x760")
janela.title("Photoshop da Julia")
janela.config(bg="#141414")
janela.resizable(False, False)
'''# Define o modo fullscreen
janela.attributes('-fullscreen', True)

# Remove a barra de título (opcional)
janela.overrideredirect(False)
def fechar():
    pass
# Cria a barra de título personalizada
barra_titulo = ctk.CTkFrame(janela, height=40, corner_radius=0, bg_color="#333333")
barra_titulo.pack(fill="x", side="top")

# Adiciona um título à barra de título
titulo = ctk.CTkLabel(barra_titulo, text="Minha Janela Fullscreen", text_color="white", font=("Arial", 14))
titulo.pack(side="left", padx=10)

# Adiciona um botão de fechar à barra de título
botao_fechar = ctk.CTkButton(barra_titulo, text="X", text_color="white", command=fechar, corner_radius=10)
botao_fechar.pack(side="right", padx=10)

# Cria o conteúdo da janela abaixo da barra de título
conteudo = ctk.CTkLabel(janela, text="Conteúdo da janela", font=("Arial", 20))
conteudo.pack(pady=50)'''


'''funções de interação com a interface e comunicação com o back-end'''
def setValorJanela(value):
    my_labelJanela.configure(text=int(value))
    global VALORJANELA 
    VALORJANELA = int(value)
    global sliderOnOff4
    sliderOnOff4 = 1


def setValorKernel(value):
    my_labelKernel.configure(text=int(value))
    global VALORKERNEL 
    VALORKERNEL = int(value)
    global sliderOnOff
    sliderOnOff = 1

def setValorLimiar(value):
    my_labelLimiar.configure(text=int(value))
    global VALORLIMIAR 
    VALORLIMIAR = int(value)
    global sliderOnOff2
    sliderOnOff2 = 1

def setValorC(value):
    my_labelValorC.configure(text=int(value))
    global VALORVALORC 
    VALORVALORC = int(value)
    global sliderOnOff3
    sliderOnOff3 = 1

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
    global sliderJanela
    global sliderKernel
    global sliderLimiar
    global sliderValorC
    positivo = 0
    global sliderOnOff
    global sliderOnOff2
    global sliderOnOff3
    global sliderOnOff4
    global FUNCAOESC2
    w = ['Binarizacao', 'Limiar Global Simples', 'Limiar Global Otsu', 'Limiar Adapt Media', 'Limiar Adapt Otsu', 'Limiar Adapt Bernsen']
    z = ['Fechamento', 'Abertura', 'Dilatacao', 'Erosao']
    #elif sliderOnOff == 0 or sliderOnOff2 == 0 and sliderOnOff3 == 0 and sliderOnOff4 == 0:
    if img_cv is None:
        popupJanela(f'Carregue uma imagem.','Ok', 0)
    
    else:


        if FUNCAOESC == 'Gaussiano' and sliderOnOff:
            #number_of_steps=126 tem que fazer conta tipo como é de 3 a 255, fica (255 -3) / 126 pro slide pular de 2 em 2
            #sliderKernel.configure(from_=3, to=7, number_of_steps=2)#desbloqueia slide após escolher uma opção, fazer personalizado
            filtered_img = filtroGaussiano(VALORKERNEL, img_cv)
            img_cv=filtered_img
            print(VALORKERNEL)
            #sliderOnOff = 0
            positivo = 1
            FUNCAOESC2.append(FUNCAOESC)
            # Exibe a imagem editada
        elif FUNCAOESC == 'Media' and sliderOnOff:
            #number_of_steps=126 tem que fazer conta tipo como é de 3 a 255, fica (255 -3) / 126 pro slide pular de 2 em 2
            #sliderKernel.configure(from_=3, to=7, number_of_steps=2, state="normal")#desbloqueia slide após escolher uma opção, fazer personalizado
            #filtered_img = filtroGaussiano(VALORJANELA, img_cv)
            filtered_img = filtroMedia(VALORKERNEL, img_cv)
            img_cv=filtered_img
            #sliderOnOff = 0
            positivo = 1
            FUNCAOESC2.append(FUNCAOESC)

            # Exibe a imagem editada
        elif FUNCAOESC == 'Mediana' and sliderOnOff:
            filtered_img = filtroMediana(VALORKERNEL, img_cv)
            img_cv=filtered_img
            positivo = 1
            FUNCAOESC2.append(FUNCAOESC)


        elif FUNCAOESC == 'Sobel' and sliderOnOff:
            filtered_img = filtroSobel(VALORKERNEL, img_cv)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            
            positivo = 1
            print('Entrei sobel')
            FUNCAOESC2.append(FUNCAOESC)

        elif FUNCAOESC == 'Laplaciano' and sliderOnOff:
            filtered_img = filtroLaplaciano(VALORKERNEL, img_cv)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            
            positivo = 1
            print('laplace')
            FUNCAOESC2.append(FUNCAOESC)

        elif FUNCAOESC == 'Binarizacao' and sliderOnOff2:
            #sliderLimiar.configure(state="normal")
            print(f'limiar = {VALORLIMIAR}')
            filtered_img = escalaDeCinza(img_cv)
            filtered_img = binarizacao(VALORLIMIAR, filtered_img)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('Entrei bina')
            FUNCAOESC2.append(FUNCAOESC)

        elif FUNCAOESC == 'Limiar Global Simples' and sliderOnOff2:
            print(f'ss {VALORLIMIAR} {filtered_img} {filtered_img.shape[0]}')
            filtered_img = escalaDeCinza(filtered_img)
            filtered_img = limiarizacaoGlobal(VALORLIMIAR, filtered_img, filtered_img.shape[0], filtered_img.shape[1])
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('Entrei LGS')
            FUNCAOESC2.append(FUNCAOESC)

        elif FUNCAOESC == 'Limiar Global Otsu':
            print(f'ss {VALORLIMIAR} {filtered_img} {filtered_img.shape[0]}')
            filtered_img = escalaDeCinza(filtered_img)
            filtered_img = metodoOtsu(filtered_img)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('Entrei Otsu')
            FUNCAOESC2.append(FUNCAOESC)

        elif FUNCAOESC == 'Limiar Adapt Media' and sliderOnOff3 and sliderOnOff4:
            filtered_img = escalaDeCinza(filtered_img)
            filtered_img = limiarizacaoAdaptativaMedia(filtered_img, VALORJANELA, VALORVALORC)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('Entrei Adap Media')
            FUNCAOESC2.append(FUNCAOESC)

        elif FUNCAOESC == 'Limiar Adapt Otsu' and sliderOnOff4:
            filtered_img = escalaDeCinza(filtered_img)
            filtered_img = limiarizacaoAdaptativaSemPaddingOtsu(filtered_img, VALORJANELA)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            FUNCAOESC2.append(FUNCAOESC)

            print('Entrei Adap Otsu')
        elif FUNCAOESC == 'Limiar Adapt Bernsen' and sliderOnOff4:
            filtered_img = escalaDeCinza(filtered_img)
            filtered_img = limiarizacaoAdaptativaMBernsen(filtered_img, VALORJANELA)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('Entrei Adap Bernsen')
            FUNCAOESC2.append(FUNCAOESC)


        elif FUNCAOESC == 'Erosao' and sliderOnOff4 and any(item in w for item in FUNCAOESC2):
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_RGB2BGR)
            filtered_img = escalaDeCinza(img_cv)
            filtered_img = erosao(filtered_img, VALORJANELA)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('Erosao')
            FUNCAOESC2.append(FUNCAOESC)

        
        elif FUNCAOESC == 'Dilatacao' and sliderOnOff4 and  any(item in w for item in FUNCAOESC2):
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_RGB2BGR)
            filtered_img = escalaDeCinza(img_cv)
            filtered_img = dilatacao(filtered_img, VALORJANELA)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('dilata')
            FUNCAOESC2.append(FUNCAOESC)

        
        elif FUNCAOESC == 'Abertura' and sliderOnOff4 and  any(item in w for item in FUNCAOESC2):
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_RGB2BGR)
            filtered_img = escalaDeCinza(img_cv)
            filtered_img = abertura(filtered_img, VALORJANELA)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('abre')
            FUNCAOESC2.append(FUNCAOESC)

        elif FUNCAOESC == 'Fechamento' and sliderOnOff4 and any(item in w for item in FUNCAOESC2):
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_RGB2BGR)
            filtered_img = escalaDeCinza(img_cv)
            filtered_img = fechamento(filtered_img, VALORJANELA)
            img_cv = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
            positivo = 1
            print('fecha')
            FUNCAOESC2.append(FUNCAOESC)

        else:
            if img_cv is None:
                popupJanela(f'Carregue uma imagem.','Ok', 0)
            else:
                print()
                print(f'qq{FUNCAOESC2} qq{FUNCAOESC}')
                if not any(item in w for item in FUNCAOESC2) and FUNCAOESC in z:
                    popupJanela(f'Aplique uma operação de Segmentação','Entendi', 1)
                elif sliderOnOff == 0 or sliderOnOff2 == 0 and sliderOnOff3 == 0 and sliderOnOff4 == 0:
                    popupJanela(f'Escolha uma propriedade e tente novamente.','Entendi', 1)

        print(FUNCAOESC)
        if positivo:
            print(f'entrei')
            display_image(filtered_img, original=False) 



def load_image():
    global img_cv
    global FUNCAOESC2
    FUNCAOESC2.clear()
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

def salvarImagem():
        
    if img_pil is None:
        popupJanela('Carregue uma Imagem', 'Ok',0)    
    else:
        nomeArquivo = filedialog.asksaveasfile(mode='w', defaultextension='jpg')
   
        if nomeArquivo is None:
            return
   
        img_pil.save(nomeArquivo)

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
        case 'MF':
            nomeImagemTop = 'hoverTopMF.png'
            nomeImagemBottom = 'hoverBottomMF.png'
        

    hoverTop = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemTop),
                                  size=(180, 3))
    # display image with a CTkLabel
    hoverTop_label = ctk.CTkLabel(frameEsquerdo, image=hoverTop, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverTop_label.place(x=xF + 16,y= yF + 1) 
    
    hoverBottom = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemBottom),
                                  size=(180, 3))
    
    # display image with a CTkLabel
    hoverBottom_label = ctk.CTkLabel(frameEsquerdo, image=hoverBottom, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverBottom_label.place(x=xF + 16,y=yF + 20) 

def hoverMenuGeral(xF, yF):
    global hoverBottom_label, hoverTop_label
    nomeImagemTop = ''
    nomeImagemBottom = ''
    pathImagem = "C:/Users/julia/Downloads/"
    nomeImagemTop = 'hoverTopMG.png'
    nomeImagemBottom = 'hoverBottomMG.png'
    
    hoverTop = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemTop), size=(168, 3))
    # display image with a CTkLabel
    hoverTop_label = ctk.CTkLabel(frameEsquerdo, image=hoverTop, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverTop_label.place(x = xF + 30,y = yF + 4) #69 
    
    hoverBottom = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemBottom), size=(168, 3))
    
    # display image with a CTkLabel
    hoverBottom_label = ctk.CTkLabel(frameEsquerdo, image=hoverBottom, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverBottom_label.place(x = xF + 30, y = yF + 25) #90


def leave(v):
    hoverTop_label.destroy()
    hoverBottom_label.destroy()

def leaveAlt(v):
    hoverTop_label.destroy()
    hoverBottom_label.destroy()
    print('Entre??')
    labelAltProp.destroy()


def hoverBotaoPropriedades(xF, yF):
    global hoverBottom_label, hoverTop_label, labelAltProp
    nomeImagemTop = ''
    nomeImagemBottom = ''
    pathImagem = "C:/Users/julia/Downloads/"
    nomeImagemTop = 'hoverTopMG.png'
    nomeImagemBottom = 'hoverBottomMG.png'
    
    hoverTop = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemTop), size=(33, 3))
    # display image with a CTkLabel
    hoverTop_label = ctk.CTkLabel(janela, image=hoverTop, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverTop_label.place(x = xF + 30,y = yF + 5) #69 
    
    hoverBottom = ctk.CTkImage(light_image=Image.open(pathImagem + nomeImagemBottom), size=(33, 3))
    
    # display image with a CTkLabel
    hoverBottom_label = ctk.CTkLabel(janela, image=hoverBottom, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",width=0,height=0)
    hoverBottom_label.place(x = xF + 30, y = yF + 35) #90

    labelAltProp = ctk.CTkLabel(janela, text='Propriedades',bg_color="#1c1c1c", fg_color="#1c1c1c",width=2, height=2,font=fontD, text_color="#848484",padx=5,pady=5,corner_radius=1)
    labelAltProp.place(x = xF - 64, y = yF + 30)


def LG():
    global btnSimples, btnOtsu, btnMedia, btnBernsen
    
    btnSimples = ctk.CTkButton(janela,text='Simples',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Global Simples'), text_color="#fefefe")
    btnSimples.place(x=231,y = 442)#

    #Para aplicar o efeito de hover
    btnSimples.bind("<Enter>", command=lambda event: hover(231,442,'SG'))
    btnSimples.bind("<Leave>", command=leave)

    btnOtsu = ctk.CTkButton(janela,text='Otsu',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Global Otsu'), text_color="#fefefe")
    btnOtsu.place(x=231,y = 472)#
    
    #Para aplicar o efeito de hover
    btnOtsu.bind("<Enter>", command=lambda event: hover(231,472,'SG'))
    btnOtsu.bind("<Leave>", command=leave)

def LA():
    global btnSimples, btnOtsu, btnMedia, btnBernsen
    
    btnMedia = ctk.CTkButton(janela,text='Média',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Media'), text_color="#fefefe")
    btnMedia.place(x=231,y = 442)#

    #Para aplicar o efeito de hover
    btnMedia.bind("<Enter>", command=lambda event: hover(231,442,'SG'))
    btnMedia.bind("<Leave>", command=leave)

    btnOtsu = ctk.CTkButton(janela,text='Otsu',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Otsu'), text_color="#fefefe")
    btnOtsu.place(x=231,y = 472)#
    
    #Para aplicar o efeito de hover
    btnOtsu.bind("<Enter>", command=lambda event: hover(231,472,'SG'))
    btnOtsu.bind("<Leave>", command=leave)

    btnBernsen = ctk.CTkButton(janela,text='Bernsen',bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc('Limiar Adapt Bernsen'), text_color="#fefefe")
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
        elif tipo == 'LA':
            LA()
            
    
            
   

   # btnLimiarG = ctk.CTkButton(janela,text="Simples",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, command=lambda:setFuncaoEsc("Limiar Global Simples"))
   # btnLimiarG.place(x=230,y=472)#

def menuPropriedades():
    global btnPropriedade, sliderJanela, my_labelJanela, my_labelNomeJanela, sliderLimiar, my_labelLimiar, my_labelNomeLimiar, sliderValorC, my_labelValorC,my_labelNomeValorC, frameDireito, sliderKernel, my_labelKernel, my_labelNomeKernel

    frameDireito = ctk.CTkLabel(master=janela, width=300,height=327, fg_color="#1c1c1c", bg_color="#1c1c1c",text='')
    frameDireito.place(x=1145,y=50)
    '''Menu Propriedades'''
    marcadorProp = ctk.CTkImage(Image.open("C:/Users/julia/Downloads/propriedades.png"), size=(24, 24))

    #Botão de abrir e fechar o menu
    btnPropriedade = ctk.CTkButton(janela,text="Propriedades",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command = fecharMenuPropriedades, text_color="#848484",image=marcadorProp, font=fontD, hover=False)
    btnPropriedade.place(x=1150,y=60)
    btnPropriedade.configure(cursor="arrow")
    #Para aplicar o efeito de hover
    btnPropriedade.bind("<Enter>", command=lambda event: hoverMenuGeral(1150, 60))
    btnPropriedade.bind("<Leave>", command=leaveAlt)



    #Slider de tamanho da janela (kernel)
    sliderKernel = ctk.CTkSlider(janela,from_=3, to=7, width=200,height=18, button_color="#9518f5", button_hover_color="#A131F6", progress_color="#9518f5", command=setValorKernel, bg_color="#1c1c1c", number_of_steps=2)
    sliderKernel.place(x=1185,y=100)
    sliderKernel.set(3)

    #Label que exibe o valor atual do slide
    my_labelKernel = ctk.CTkLabel(janela, text=int(sliderKernel.get()), bg_color="#1c1c1c", fg_color="#1c1c1c", font=fontB)
    my_labelKernel.place(x=1395,y=93)

    #Label que exibe o nome do slide
    my_labelNomeKernel = ctk.CTkLabel(janela, text="Kernel - Filtros", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#f7f7f7", font=fontC, height=0)
    my_labelNomeKernel.place(x=1185,y=127)

     #Slider de tamanho da janela (kernel)
    sliderJanela = ctk.CTkSlider(janela,from_=3, to=255, width=200,height=18, button_color="#9518f5", button_hover_color="#A131F6", progress_color="#9518f5", command=setValorJanela, bg_color="#1c1c1c")
    sliderJanela.place(x=1185,y=170)
    sliderJanela.set(3)

    #Label que exibe o valor atual do slide
    my_labelJanela = ctk.CTkLabel(janela, text=sliderJanela.get(), bg_color="#1c1c1c", fg_color="#1c1c1c", font=fontB)
    my_labelJanela.place(x=1395,y=163)

    #Label que exibe o nome do slide
    my_labelNomeJanela = ctk.CTkLabel(janela, text="Janela - Segmentação e Morfologia", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#f7f7f7", font=fontC, height=0)
    my_labelNomeJanela.place(x=1185,y=197)


    print(FUNCAOESC)
    #Executa uma função de processamento de imagem ao soltar o mouse do slide
    #sliderJanela.bind("<ButtonRelease-1>",command=a)

    #Slider do Limiar
    sliderLimiar = ctk.CTkSlider(janela,from_=0, to=255, width=200,height=18,button_color="#9518f5", button_hover_color="#A131F6", progress_color="#9518f5", command=setValorLimiar, state="normal", bg_color="#1c1c1c")
    sliderLimiar.place(x=1185,y=240)
    #inicia o slide na posição 0
    sliderLimiar.set(0)
    #Label que exibe o valor atual do slide
    my_labelLimiar = ctk.CTkLabel(janela, text=sliderLimiar.get(), bg_color="#1c1c1c", fg_color="#1c1c1c", font=fontD)
    my_labelLimiar.place(x=1395,y=233)
    #Executa uma função de processamento de imagem ao soltar o mouse do slide
    #sliderLimiar.bind("<ButtonRelease-1>",command=a)
    #Label que exibe o nome do slide
    my_labelNomeLimiar = ctk.CTkLabel(janela, text="Limiar", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#f7f7f7", font=fontC, height=0)
    my_labelNomeLimiar.place(x=1185,y=267)

    #Slider do Valor C
    sliderValorC = ctk.CTkSlider(janela,from_=-255, to=255, width=200,height=18,button_color="#9518f5", button_hover_color="#A131F6", progress_color="#9518f5", command=setValorC, state="normal", bg_color="#1c1c1c")
    sliderValorC.place(x=1185,y=310)
    #inicia o slide na posição 0
    sliderValorC.set(0)
    #Label que exibe o valor atual do slide
    my_labelValorC = ctk.CTkLabel(janela, text=sliderValorC.get(), bg_color="#1c1c1c", fg_color="#1c1c1c", font=fontD)
    my_labelValorC.place(x=1395,y=317)
    #Executa uma função de processamento de imagem ao soltar o mouse do slide
    #sliderLimiar.bind("<ButtonRelease-1>",command=a)
    #Label que exibe o nome do slide
    my_labelNomeValorC = ctk.CTkLabel(janela, text="Valor C", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#f7f7f7", font=fontC, height=0)
    my_labelNomeValorC.place(x=1185,y=351)


def botaoPropriedades():
    iconProp = ctk.CTkImage(Image.open("C:/Users/julia/Downloads/propriedades.png"), size=(24, 24))
   # labelBotaoProp = ctk.CTkLabel(master=janela, width=40,height=5, fg_color="red", bg_color="#1c1c1c",text='')
    #labelBotaoProp.place(x=1145,y=50)
    global btnIconProp
    btnIconProp = ctk.CTkButton(master=janela, bg_color="#1c1c1c", image=iconProp, text='', fg_color="#1c1c1c", width=15,height=15, hover=False, command=abrirMenuPropriedades, corner_radius=0)
    btnIconProp.place(x = 1408, y = 65)
    btnIconProp.configure(cursor="arrow")

    #Para aplicar o efeito de hover
    btnIconProp.bind("<Enter>", command=lambda event: hoverBotaoPropriedades(1377,60))
    btnIconProp.bind("<Leave>", command=leaveAlt)

def abrirMenuPropriedades():
    btnIconProp.destroy()
    leave('')
    leaveAlt('')
    menuPropriedades()

def fecharMenuPropriedades():
    btnPropriedade.destroy()
    sliderJanela.destroy()
    my_labelJanela.destroy()
    my_labelNomeJanela.destroy()
    sliderKernel.destroy()
    my_labelKernel.destroy()
    my_labelNomeKernel.destroy()
    sliderLimiar.destroy()
    my_labelLimiar.destroy()
    my_labelNomeLimiar.destroy()
    sliderValorC.destroy()
    my_labelValorC.destroy()
    my_labelNomeValorC.destroy()
    leave('')
    frameDireito.destroy()
    botaoPropriedades()
    print('clicou')

def fecharPopUp(popUp, textLabel, btn):
    
    if isinstance(textLabel, list):
        for t in textLabel:
            t.destroy()
    else:
        textLabel.destroy()

    btn.destroy()
    popUp.destroy()
    global cliquePOPUP1, cliquePOPUP2
    cliquePOPUP1 = 0
    cliquePOPUP2 = 0

def ajudaProp():
    global cliquePOPUP2
    if cliquePOPUP2 == 0:
        cliquePOPUP2+=1
        popup = ctk.CTkToplevel(janela, fg_color="#141414")
        popup.geometry('900x350')
        popup.title('Opções de edição e suas propriedades')
        popup.resizable(0,0)
        #títulos
        fontTitulo = ctk.CTkFont(family="Inconsolata", size = 14, weight="bold")
        tituloLabel = ctk.CTkLabel(popup, text='Propriedades Disponíveis de Cada Opção de Edição', anchor='n', justify='center', font=fontTitulo, text_color="#9518f5")
        tituloLabel.grid(row=1, column= 2, padx=(0,0), pady=(10,10),)

        fontAux1 = ctk.CTkFont(family="Inconsolata",size=14, weight="bold")
        fontAux2 = ctk.CTkFont(family="Inconsolata",size=13, weight="bold")

        pbLabel = ctk.CTkLabel(popup, text='Filtro Passa-Baixa', text_color="#848484", font=fontAux1, anchor='w', justify='left')
        pbLabel.grid(row = 2, column=0, padx=(10,10), pady=(10,0), sticky ='W')
        kernelLabel = ctk.CTkLabel(popup, text='Kernel - Filtros', text_color="#fefefe", font=fontAux2, anchor='w', justify='left')
        kernelLabel.grid(row = 3, column=0, padx=(10,10), pady=(0,0), sticky = 'W')

        paLabel = ctk.CTkLabel(popup, text='Filtro Passa-Alta', text_color="#848484", font=fontAux1, anchor='w', justify='left')
        paLabel.grid(row = 2, column=1, padx=(10,10), pady=(10,0), sticky = 'W')
        kernelLabel = ctk.CTkLabel(popup, text='Kernel - Filtros', text_color="#fefefe", font=fontAux2, anchor='w', justify='left')
        kernelLabel.grid(row = 3, column=1, padx=(10,10), pady=(0,0), sticky = 'W')

        sgLabel = ctk.CTkLabel(popup, text='Segmentação', text_color="#848484", font=fontAux1, anchor='w', justify='left')
        sgLabel.grid(row = 2, column=2,padx=(10,10),pady=(10,0), sticky = 'W')
        janelaLabel = ctk.CTkLabel(popup, text='Janela - Segmentação e Morfologia', text_color="#fefefe", font=fontAux2, anchor='w', justify='left')
        janelaLabel.grid(row = 3, column=2, padx=(10,10),pady=(10,0), sticky = 'W')
        limiarLabel = ctk.CTkLabel(popup, text='Limiar', text_color="#fefefe", font=fontAux2, anchor='w', justify='left')
        limiarLabel.grid(row = 4, column=2, padx=(10,10),pady=(10,0), sticky = 'W')
        cLabel = ctk.CTkLabel(popup, text='Valor C', text_color="#fefefe", font=fontAux2, anchor='w', justify='left')
        cLabel.grid(row = 5, column=2, padx=(10,10),pady=(10,0), sticky = 'W')
        biLabel = ctk.CTkLabel(popup, text='Na binarização, a janela não é considerada', text_color="#B762F8", font=fontAux2, anchor='w', justify='left')
        biLabel.grid(row = 6, column=2, padx=(10,10),pady=(10,0), sticky = 'W')
        ccLabel = ctk.CTkLabel(popup, text='O valor C é usado somente na limiarização adaptativa média', text_color="#B762F8", font=fontAux2, anchor='w', justify='left')
        ccLabel.grid(row = 7, column=2, padx=(10,10),pady=(10,0), sticky = 'W')

        mfLabel = ctk.CTkLabel(popup, text='Morfologia', text_color="#848484", font=fontAux1, anchor='w', justify='left')
        mfLabel.grid(row = 2, column=3, padx=(10,10),pady=(10,0), sticky = 'W')
        janelaLabel = ctk.CTkLabel(popup, text='Janela - Segmentação e Morfologia', text_color="#fefefe", font=fontAux2, anchor='w', justify='left')
        janelaLabel.grid(row = 3, column=3, padx=(10,10),pady=(10,0), sticky = 'W')
        
        btn = ctk.CTkButton(popup, text='Ok', bg_color="#9518f5", fg_color="#9518f5", corner_radius=1, hover_color="#6D08BA", font=fontAux1, command=lambda:fecharPopUp(popup, [pbLabel,kernelLabel,paLabel, sgLabel, janelaLabel,limiarLabel, cLabel, biLabel, mfLabel], btn))
        btn.grid(row = 8, column=2, padx=(10,10),pady=(30,10))

        popup.after(100, lambda: popup.lift())


def hoverAjuda(xF, yF, btnAjuda):
    btnAjuda.configure(text_color="#9518f5", border_color="#9518f5")

def leaveHoverAjuda(btnAjuda):
    btnAjuda.configure(text_color="#b762f8", border_color="#b762f8")



def popupJanela(msg, msgBotao, op):
    #POP-UP
    global cliquePOPUP1
    print(f'tt {cliquePOPUP1}')
    if cliquePOPUP1 == 0:
        cliquePOPUP1+=1
        popup = ctk.CTkToplevel(janela, fg_color="#141414")
        popup.geometry('380x200')
        popup.title('Aviso')
        popup.resizable(0,0)
        textLabel = ctk.CTkLabel(popup, text=msg, text_color="#fefefe", font=fontB)
        textLabel.pack(pady=20,padx = 20)
        fontE = ctk.CTkFont(family="Inconsolata",size=13, weight="bold")
        fontF = ctk.CTkFont(family="Inconsolata",size=14, weight="bold")
        
        btn = ctk.CTkButton(popup, text=msgBotao, bg_color="#9518f5", fg_color="#9518f5", corner_radius=1, hover_color="#6D08BA", font=fontF, command=lambda:fecharPopUp(popup,textLabel, popup))
        btn.pack()
        popup.after(100, lambda: popup.lift())

        if op:
           pass
        


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
salvarImagemIcon = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/file_download_24dp.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/file_download_24dp.png"),
                                  size=(24, 24))


btnCarregarImagem = ctk.CTkButton(janela,text="Carregar Imagem",image=carregarImagem, bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=load_image, font=fontB, hover=False, text_color="#fefefe")

btnCarregarImagem.place(x=10,y=65)
#btnCarregarImagem.configure(cursor="hand2")

btnSalvarImagem = ctk.CTkButton(janela,text="Salvar Imagem",image=salvarImagemIcon,bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontB,hover=False, command= salvarImagem, text_color="#fefefe")
btnSalvarImagem.place(x=10,y=105)

#Para aplicar o efeito de hover
btnCarregarImagem.bind("<Enter>", command=lambda event: hoverMenuGeral(10,65))
btnCarregarImagem.bind("<Leave>", command=leave)

#Para aplicar o efeito de hover
btnSalvarImagem.bind("<Enter>", command=lambda event: hoverMenuGeral(10,105))
btnSalvarImagem.bind("<Leave>", command=leave)



#Para aplicar o efeito de hover
#btnSalvarImagem.bind("<Enter>", command=lambda event: hoverMenuGeral(10,105))
#btnSalvarImagem.bind("<Leave>", command=leave)
#separador de seção
separador = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  size=(220, 2))
separador_label = ctk.CTkLabel(frameEsquerdo, image=separador, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",height=2).place(x=0,y=145)  




'''Menu Passa-Baixa'''
#bullets points
marcadorPB = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/marcadorPassaBaixa.png"),
                                  size=(8, 8))

btnGaussiano = ctk.CTkButton(janela,text="Gaussiano",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Gaussiano"), font=fontD,hover=False,image=marcadorPB, text_color="#fefefe")
btnGaussiano.place(x=12,y=181)
#Para aplicar o efeito de hover
btnGaussiano.bind("<Enter>", command=lambda event: hover(12,181,'PB'))
btnGaussiano.bind("<Leave>", command=leave)

btnMedia = ctk.CTkButton(janela,text="Média",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Media"), font=fontD, image=marcadorPB, hover=False, text_color="#fefefe")
btnMedia.place(x=12,y=211)

#Para aplicar o efeito de hover
btnMedia.bind("<Enter>", command=lambda event: hover(12,211,'PB'))
btnMedia.bind("<Leave>", command=leave)

btnMediana = ctk.CTkButton(janela,text="Mediana",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Mediana"), font=fontD, image=marcadorPB, hover=False, text_color="#fefefe")
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

btnSobel = ctk.CTkButton(janela,text="Sobel",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Sobel"), font=fontD,hover=False,image=marcadorPA, text_color="#fefefe")
btnSobel.place(x=12,y=306)
#Para aplicar o efeito de hover
btnSobel.bind("<Enter>", command=lambda event: hover(12,306,'PA'))
btnSobel.bind("<Leave>", command=leave)

btnLaplaciano = ctk.CTkButton(janela,text="Laplaciano",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Laplaciano"), font=fontD, image=marcadorPA, hover=False, text_color="#fefefe")
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
btnBinarizacao = ctk.CTkButton(janela,text="Binarização",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", command=lambda:setFuncaoEsc("Binarizacao"), font=fontD, image=marcadorSG, hover=False, text_color="#fefefe")
btnBinarizacao.place(x=12,y=402)

#Para aplicar o efeito de hover
btnBinarizacao.bind("<Enter>", command=lambda event: hover(12,402,'SG'))
btnBinarizacao.bind("<Leave>", command=leave)

btnLimiarG = ctk.CTkButton(janela,text="Limiarização Global",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, hover=False, text_color="#fefefe")
btnLimiarG.place(x=12,y=432)#command=lambda:setFuncaoEsc("Limiar Global")
setaDir = ctk.CTkImage(Image.open("C:/Users/julia/Downloads/setaDireita.png"), size=(24, 24))
setaDir_label = ctk.CTkLabel(frameEsquerdo,width=0, height=0,bg_color="#1c1c1c", fg_color="#1c1c1c",image=setaDir, text='')
setaDir_label.place(x=160, y=431.5)
setaDir_label = ctk.CTkLabel(frameEsquerdo,width=0, height=0,bg_color="#1c1c1c", fg_color="#1c1c1c",image=setaDir, text='')
setaDir_label.place(x=185, y=463)
#Para aplicar o efeito de hover
btnLimiarG.bind("<Enter>", command=lambda event: hover(12,432,'SG'))
btnLimiarG.bind("<Leave>", command=leave)

btnLimiarA = ctk.CTkButton(janela,text="Limiarização Adaptativa",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", font=fontD, image=marcadorSG, text_color="#fefefe",hover=False)
btnLimiarA.place(x=12,y=462)#command=lambda:setFuncaoEsc("Limiar Adaptativo")

#Para aplicar o efeito de hover
btnLimiarA.bind("<Enter>", command=lambda event: hover(12,462,'SG'))
btnLimiarA.bind("<Leave>", command=leave)

#submenu limiarização global
btnLimiarG.bind("<Button-1>", command=lambda event: abrirfecharJanelaLimiar('LG', 'fecharLG'))

btnLimiarA.bind("<Button-1>", command=lambda event: abrirfecharJanelaLimiar('LA', 'fecharLA'))

#separador de seção
separador = ctk.CTkImage(light_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  dark_image=Image.open("C:/Users/julia/Downloads/separador.png"),
                                  size=(220, 2))
separador_label = ctk.CTkLabel(frameEsquerdo, image=separador, text="",bg_color="#1c1c1c",fg_color="#1c1c1c",height=2).place(x=0,y=492)  


'''Menu Morfologia'''
#bullets points
marcadorMF = ctk.CTkImage(Image.open("C:/Users/julia/Downloads/marcadorMorfologia.png"), size=(8, 8))

btnErosao = ctk.CTkButton(janela,text="Erosão",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", text_color="#fefefe",command=lambda:setFuncaoEsc("Erosao"), font=fontD,image=marcadorMF, hover=False)
btnErosao.place(x=12,y=528)

#Para aplicar o efeito de hover
btnErosao.bind("<Enter>", command=lambda event: hover(12,528,'MF'))
btnErosao.bind("<Leave>", command=leave)

btnDilatacao = ctk.CTkButton(janela,text="Dilatação",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", text_color="#fefefe",command=lambda:setFuncaoEsc("Dilatacao"), font=fontD,image=marcadorMF, hover=False)
btnDilatacao.place(x=12,y=558)

#Para aplicar o efeito de hover
btnDilatacao.bind("<Enter>", command=lambda event: hover(12,558,'MF'))
btnDilatacao.bind("<Leave>", command=leave)

btnAbertura = ctk.CTkButton(janela,text="Abertura",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", text_color="#fefefe",command=lambda:setFuncaoEsc("Abertura"), font=fontD,image=marcadorMF, hover=False)
btnAbertura.place(x=12,y=588)

#Para aplicar o efeito de hover
btnAbertura.bind("<Enter>", command=lambda event: hover(12,588,'MF'))
btnAbertura.bind("<Leave>", command=leave)

btnFechamento = ctk.CTkButton(janela,text="Fechamento",bg_color="#1c1c1c", width=4, height=5, fg_color="#1c1c1c", text_color="#fefefe",command=lambda:setFuncaoEsc("Fechamento"), font=fontD,image=marcadorMF, hover=False)
btnFechamento.place(x=12,y=618)

#Para aplicar o efeito de hover
btnFechamento.bind("<Enter>", command=lambda event: hover(12,618,'MF'))
btnFechamento.bind("<Leave>", command=leave)


fontG = ctk.CTkFont(family="Inconsolata",size=14, weight="bold")
btnAjuda = ctk.CTkButton(frameEsquerdo, text='Ajuda', font=fontG, corner_radius=1, hover=False, bg_color="#b762f8",text_color="#b762f8", fg_color="#141414", command=ajudaProp, height=10, width=10, border_color="#b762f8",border_width=2,border_spacing=5)
btnAjuda.place(x=12, y = 698)

#Para aplicar o efeito de hover
btnAjuda.bind("<Enter>", command=lambda event: hoverAjuda(btnAjuda.winfo_x(),btnAjuda.winfo_y(), btnAjuda))
btnAjuda.bind("<Leave>", command=lambda e: leaveHoverAjuda(btnAjuda))

'''Menu Propriedades'''
botaoPropriedades()



'''Título de cada seção'''
labelPB = ctk.CTkLabel(frameEsquerdo,text="Filtros Passa-Baixa", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#848484", font=fontC).place(x=10,y=155)

labelPA = ctk.CTkLabel(frameEsquerdo,text="Filtros Passa-Alta", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#848484", font=fontC).place(x=10,y=281)

labelSeg = ctk.CTkLabel(frameEsquerdo,text="Segmentação", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#848484", font=fontC).place(x=10,y=376)

labelMF = ctk.CTkLabel(frameEsquerdo,text="Morfologia", bg_color="#1c1c1c", fg_color="#1c1c1c", text_color="#848484", font=fontC).place(x=10,y=502)



'''
Comentários Gerais
#number_of_steps = 10 vai de 10 em 10

#janela.maxsize() pode redimensionar até tanto de tamanho
#janela.resizable() permite ou proibe redimensionar



#janela.attributes("-fullscreen", True)
#janela.state('zoomed')
#resolucaoJanelaUsuario = str(janela.winfo_screenwidth()) + 'x' + str(janela.winfo_screenheight())

'''    








janela.mainloop() 

