## Criação dos Armarios  ##
import json
from datetime import datetime, timedelta

armarios = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
    9: None,
    10: None,
    11: None,
    12: None,
    13: None,
    14: None,
    15: None,
    16: None,
    17: None,
    18: None,
    19: None,
    20: None
      }


## Salvando e Carregando os dados com o JSON ##

def salvar_dados():
    with open ('armarios.json', 'w', encoding = 'utf-8') as arquivo:
        json.dump(armarios, arquivo, ensure_ascii = False, indent = 4) 


def carregar_dados():

    global armarios

    try:
        with open ('armarios.json', 'r', encoding = 'utf-8') as arquivo:
            dados_json = json.load(arquivo)
            armarios = {int(chave): valor for chave, valor in dados_json.items()}

    except FileNotFoundError:

        print ('Arquivo JSON não encontrado.')


## Expiração de reservas ##

def verificar_expiracao():
    
    agora = datetime.now()

    for numero, dados in armarios.items():
        if dados is not None:
            if 'data_reserva' not in dados:
                continue
            data_reserva = datetime.fromisoformat(dados['data_reserva'])

            tempo_reserva = agora - data_reserva

            if tempo_reserva > timedelta(hours=4):

                armarios[numero] = None
                print('Armario {}: Reserva expirada! Liberando armario...'.format(numero))

    salvar_dados()


## Funções para o controle dos armarios ##

def mostrar_armarios():
    print("\n ------ Armarios Disponivies ------")
    
    for numero, dados in armarios.items():
        if dados is None:
            print ('Armario {}: 🟩 Disponivel '.format(numero))
        else:
            print ('Armario {}: 🟥 Reservado por - {}'.format(numero, dados["nome"]))


def reservar_armarios():
    numero_armario = pedir_numero_armario()

   
    if armarios[numero_armario] is None:
        nome_aluno = input("Digite o nome do aluno: ")
        senha_aluno = input("Digite a senha do armario: ")


        armarios [numero_armario] = {
            'nome': nome_aluno,
            'senha': senha_aluno,
            'data_reserva': datetime.now().isoformat()
        }
        
        salvar_dados()
        
        print ('\n Armario {}: Reservado com sucesso !'.format(numero_armario))

    else:
        print ("Armario {}: Esta ocupado !".format(numero_armario))


def liberar_armarios():

    numero_armario = pedir_numero_armario()

    if armarios[numero_armario] is not None:

        confirmar = input(
            "Tem certeza que deseja liberar o armario {} ? (s/n): ".format(numero_armario)
        )

        if confirmar.lower() == 's':

            armarios[numero_armario] = None

            salvar_dados()

            print('Armario {}: Liberado com sucesso !'.format(numero_armario))

        else:
            print('Operacao cancelada !')

    else:
        print('Armario {}: Ja esta disponivel !'.format(numero_armario))


def consultar_armarios():
    numero_armario = pedir_numero_armario()
   

    if armarios[numero_armario] is not None:

         data = datetime.fromisoformat(armarios[numero_armario]['data_reserva'])
         
         print ('Armario {}:\n Reservado por: {}'.format(numero_armario, armarios[numero_armario]['nome']))
         print ('Senha do armario: {}'.format(armarios[numero_armario]['senha']))
         print('Data da reserva: {}'.format(data.strftime("%d/%m/%Y %H:%M")))

    else:
        print ('Armario {}: Esta disponivel !'.format(numero_armario))


def pedir_numero_armario():

    while True:
        try:
            numero = int(input("Digite o numero do armario: "))

            if numero not in armarios:
                print ('Armario inexistente !')
                continue

           
            return numero 
        
        except ValueError:
            print ('Opção invalida, digite apenas numeros !')


## Criação do Menu ##

carregar_dados()
verificar_expiracao()


while True:
    print (' ----- Controle de Armarios -----')
    print ('[1] - Mostrar Armarios')
    print ('[2] - Reservar Armarios')
    print ('[3] - Liberar Armarios')
    print ('[4] - Consultar Armarios')
    print ('[0] - Sair')
    print (' --------------------------------')

    opcao = input("Digite a opcao desejada: ")
    if opcao == '1':
        mostrar_armarios()
    elif opcao == '2':
        reservar_armarios()
    elif opcao == '3':
        liberar_armarios()
    elif opcao == '4':
        consultar_armarios()
    elif opcao == '0':
        print ('Saindo do programa...')
        break
    else:
        print ('Opcao invalida ! Digite novamente.')






