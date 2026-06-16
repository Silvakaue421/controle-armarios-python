import tkinter as tk
import Controle_Armarios as sistema
from tkinter import messagebox

sistema.carregar_dados()

## Criação da Janela ##

janela = tk.Tk()
janela.configure(bg="#EEF2F7")


janela.title('Controle de Armários')
janela.geometry("600x650")
janela.resizable(False, False)

titulo = tk.Label (
    janela,
    text = '🔐 Sistema de Controle de Armários',
    font=("Segoe UI", 24, "bold"),
    bg="#EEF2F7",
    fg="#1E293B"
)  

titulo.pack (pady = (20,10))

label_estatisticas = tk.Label(
    janela,
    text="",
    font=("Segoe UI", 11, "bold"),
    bg="#EEF2F7",
    fg="#1E293B",
    padx=15,
    pady=8
)

label_estatisticas.pack()

## Dicionario para os botoes ##

botoes_armarios = {}

## Atualição dos armarios ##
def atualizar_estatisticas():

    ocupados = 0

    for dados in sistema.armarios.values():

        if dados is not None:
            ocupados += 1

    livres = len(sistema.armarios) - ocupados

    label_estatisticas.config(
        text=f" Ocupados: {ocupados} |  Livres: {livres}"
    )


def atualizar_armarios():


    for numero in sistema.armarios:

        if sistema.armarios[numero] is None:
            botoes_armarios[numero].config(bg="#22C55E")
        else:
            botoes_armarios[numero].config(bg="#EF4444")

    atualizar_estatisticas()       

## Criação das funçoes de clicar ##
from datetime import datetime

def reservar_armario_interface(numero, nome, senha, janela_armario):

    if nome.strip() == "" or senha.strip() == "":
        messagebox.showerror(
            "Erro",
            "Preencha nome e senha."
            )
        return

    sistema.armarios[numero] = {
        "nome": nome,
        "senha": senha,
        "data_reserva": datetime.now().isoformat()

    }
     
    sistema.salvar_dados()
    
    atualizar_armarios()

    messagebox.showinfo(
    "Sucesso",
    f"Armário {numero} reservado com sucesso!")
    
    janela_armario.destroy()

def liberar_armario_interface(numero, janela_armario):

    sistema.armarios[numero] = None
    
    sistema.salvar_dados()

    atualizar_armarios()
    
    messagebox.showinfo(
    "Sucesso",
    f"Armário {numero} liberado com sucesso!")

    janela_armario.destroy()


def clicar_armario(numero):

    janela_armario = tk.Toplevel(janela)
    janela_armario.configure(bg="#F4F6F9")

    janela_armario.title(f"Armário {numero}")

    janela_armario.transient(janela)
    janela_armario.grab_set()

    largura_janela = 300
    altura_janela = 200

    janela.update_idletasks()

    x = janela.winfo_x() + (janela.winfo_width() // 2) - (largura_janela // 2)
    y = janela.winfo_y() + (janela.winfo_height() // 2) - (altura_janela // 2)

    janela_armario.geometry( f"{largura_janela}x{altura_janela}+{x}+{y}")
    
    
    if sistema.armarios[numero] is not None:
        data = datetime.fromisoformat(sistema.armarios[numero]['data_reserva'])
        tk.Label(
            janela_armario,
            text=f"Reservado em",
            font=("Segoe UI", 10, "bold"),
            bg="#F4F6F9"

            ).pack()
       
        tk.Label(
            janela_armario,
            text=data.strftime("%d/%m/%Y às %H:%M"),
            font=("Segoe UI", 10),
            bg="#F4F6F9"
            
            ).pack(pady=(0, 10))
        
        tk.Label(
            janela_armario,
            text = f"👤 Nome do Aluno: {sistema.armarios[numero]['nome']}",
            font=("Segoe UI", 10, "bold"),
            bg="#F4F6F9"
            ).pack(pady=(0, 10))
        tk.Label(
            janela_armario,
            text = f"🔒 Senha do Aluno: {sistema.armarios[numero]['senha']}",
            font=("Segoe UI", 11, "bold"),
            bg="#F4F6F9",
            

            ).pack(pady=(0,15))
        tk.Button(
            janela_armario,
            text="Liberar Armário",
            font=("Segoe UI", 10, "bold"),
            bg="#D8D7D7",
            relief="flat",
            cursor="hand2",
            width=14,

            command = lambda: liberar_armario_interface(
                numero,
                janela_armario
                )
            ).pack(pady=20)
    else:
        tk.Label(
            janela_armario,
            text="Armário disponível",
            font=("Segoe UI", 14, "bold"),
            bg="#F4F6F9"
        ).pack(pady=5)
        
        tk.Label(janela_armario,text="Nome do Aluno:").pack()
        entrada_nome = tk.Entry(janela_armario)
        entrada_nome.pack(pady=5)
        
        tk.Label(janela_armario,text="Senha do Aluno:").pack()
        entrada_senha = tk.Entry(janela_armario)
        entrada_senha.pack(pady=5)
        
        tk.Button(
            janela_armario,
            text="Reservar Armário",
            font=("Segoe UI", 10, "bold"),
            bg="#D8D7D7",
            relief="flat",
            cursor="hand2",
            width=14,

            command=lambda: reservar_armario_interface(
                numero,
                entrada_nome.get(),
                entrada_senha.get(),
                janela_armario
        )
        ).pack(pady=10)
       

## Botao de busca ##

def buscar_aluno():

    nome = entrada_busca.get().strip().lower()

    for numero, dados in sistema.armarios.items():

        if dados is not None:

            if nome in dados['nome'].lower():

                messagebox.showinfo(
                    "Resultado",
                    f"{dados['nome']} está no armário {numero}"
                )

                return

    messagebox.showwarning(
        "Resultado",
        "Aluno não encontrado."
    )

frame_busca = tk.Frame(janela, bg="#F4F6F9")
frame_busca.pack(pady=15)

entrada_busca = tk.Entry(
    frame_busca,
    font=("Segoe UI", 10),
    width=35,
    relief="solid",
    bd=1
)
entrada_busca.pack(side="left", ipady = 5)

tk.Button(
    frame_busca,
    text="🔍 Buscar",
    font=("Segoe UI", 9, "bold"),
    bg="#868686",
    fg="white",
    activebackground="#BABABA",
    relief="flat",
    cursor="hand2",
    command=buscar_aluno
).pack(side="left", padx=10)



## criaçãp dos armarios ##

frame_armarios = tk.Frame(janela, bg="#F4F6F9", bd=1, relief="solid" )
frame_armarios.pack(pady=15, padx=20, expand=True)


def criar_armarios ():
   
    for numero in sistema.armarios.keys():
        
        if sistema.armarios[numero] is None:
            cor = "#22C55E"
        else:
            cor = "#EF4444"

        botao = tk.Button(
            frame_armarios,
            text = f"Armário\n\n{numero:02}",
            width =  12,
            height = 4,
            font=("Segoe UI", 9, "bold"),
            bg = cor,
            relief="flat",
            fg="black",
            bd=0,
            cursor="hand2",
            activebackground=cor,
           
            command=lambda n=numero: clicar_armario(n)
        )
        
        botoes_armarios[numero] = botao
        
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        
        botao.grid(
            row =  linha,
            column = coluna,
            padx = 5,
            pady = 5
    )

criar_armarios()

legenda = tk.Label(
    janela,
    text="Verde = Disponível    |   Vermelho = Ocupado",
    font=("Segoe UI", 9),
    bg="#F4F6F9",
    fg="#475569"
    )
legenda.pack(side="bottom", pady=10)


atualizar_estatisticas()


janela.mainloop()
