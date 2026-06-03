from src.core.livro import Livro
from src.database.banco import conectar

# Inicialização da persistência: estabelece conexão e cria os objetos de controle
conexao = conectar()
cursor = conexao.cursor()

# Injeção de Dependência: repassa a conexão ativa para a classe Livro
# Isso permite que a classe realize operações DML (Data Manipulation Language)
Livro.conexao = conexao
Livro.cursor = cursor

# Loop principal do sistema (Runtime)
while True:
    menu = input("""
    ------- MENU ------
    Aperte [1] para cadastrar um livro
    Aperte [2] para exibir a biblioteca de livros cadastrados
    Aperte [3] para pesquisar um livro
    Aperte [4] para listar livros de um autor
    Aperte [5] para remover um livro
    Aperte [6] para atualizar um livro
    Aperte [7] para sair 
    -------------------
    """)

    if menu == '1':
        try:
            # Captura de dados via console
            nome_livro = input('Digite o nome do livro: ')
            autor_livro = input('Digite o nome do autor: ')
            ano = input('Digite o ano de lançamento: Ou pressione Enter para pular')
            editora = input('Digite a editora: Ou pressione Enter para pular')
            numero_de_paginas = input('Digite o número de páginas: Ou pressione Enter para pular')

            # Tratamento de dado opcional e conversão de tipo (casting)
            if numero_de_paginas:
                numero_de_paginas = int(numero_de_paginas)
            else:
                numero_de_paginas = None

            # Instanciação do objeto Livro na memória
            novo_livro = Livro(nome_livro, autor_livro, ano=ano, editora=editora, numero_de_paginas=numero_de_paginas)
            novo_livro.adicionar_livro()

            print(f'Livro {nome_livro} foi adicionado com sucesso.')

        except ValueError:
            # Tratamento de exceção para garantir que a aplicação não aborte por erro de input
            print('ERRO! No campo Páginas digite apenas números inteiros')
            print('Cadastramento cancelado. Tente novamente.')

    elif menu == '2':
        print("------ BIBLIOTECA -------")
        Livro.mostrar_biblioteca()

    elif menu == '3':
        busca = input("Digite o nome do livro que deseja procurar: ")
        Livro.pesquisar_livro(busca)

    elif menu == '4':
        autor_desejado = input("Digite o nome do Autor: ")
        Livro.listar_livro_por_autor(autor_desejado)

    elif menu == '5':
        nome_remover = input("Digite o nome do livro que deseja remover: ")
        Livro.remover_livro(nome_remover)

    elif menu == '6':
        # Submenu de atualização (Update)
        print("------- BIBLIOTECA -------")
        Livro.mostrar_biblioteca()
        while True:
            opcao = input("""
            Digite [1] se deseja atualizar o nome do livro
            Digite [2] se deseja atualizar o autor do livro
            Digite [3] se deseja atualizar o ano de lançamento do livro
            Digite [4] se deseja atualizar a editora do livro
            Digite [5] se deseja atualizar a quantidade de páginas do livro
            Digite [0] para voltar ao menu principal
            """)

            if opcao == "1":
                id_livro = input("Digite o ID do livro que deseja atualizar: ")
                nome_novo = input(f"Novo nome para ID {id_livro}: ").upper()
                Livro.atualizar_nome_livro(id_livro, nome_novo)
            elif opcao == "2":
                id_livro = input("Digite o ID: ")
                autor_novo = input(f"Novo autor para ID {id_livro}: ").upper()
                Livro.atualizar_autor_livro(id_livro, autor_novo)
            elif opcao == "3":
                id_livro = input("Digite o ID: ")
                ano_novo = input(f"Novo ano para ID {id_livro}: ")
                Livro.atualizar_ano_lancamento_livro(id_livro, ano_novo)
            elif opcao == "4":
                id_livro = input("Digite o ID: ")
                editora_nova = input(f"Nova editora para ID {id_livro}: ")
                Livro.atualizar_editora_livro(id_livro, editora_nova)
            elif opcao == "5":
                id_livro = input("Digite o ID: ")
                qtd_paginas_nova = input(f"Nova quantidade de páginas para ID {id_livro}: ")
                Livro.atualizar_qtd_paginas_livro(id_livro, qtd_paginas_nova)
            elif opcao == "0":
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida. Tente novamente")

    elif menu == '7':
        print("Encerrando sistema...")
        break

# Encerramento seguro de recursos
cursor.close()
conexao.close()