import pyodbc


class Livro:
    # Atributos de classe que armazenarão a instância de conexão e o cursor do banco de dados
    cursor = None
    conexao = None

    def __init__(self, nome, autor, **extras):
        """
        Método construtor da classe Livro.
        :param nome: String representando o título do livro.
        :param autor: String representando o autor do livro.
        :param extras: Dicionário de argumentos variáveis para atributos opcionais.
        """
        self.nome = nome
        self.autor = autor
        self.extras = extras

    @classmethod
    def mostrar_biblioteca(cls):
        """
        Realiza uma consulta de seleção (SELECT) para listar todos os registros da tabela Livros.
        """
        # Execução da query SQL solicitando colunas específicas para otimização de performance
        cls.cursor.execute("SELECT id, nome, autor FROM Livros")

        # Recuperação de todos os registros retornados pela consulta
        livros = cls.cursor.fetchall()

        print(f"Total de livros cadastrados: {len(livros)}")

        # Iteração sobre os registros para exibição formatada no console
        for id, nome, autor in livros:
            print(id, "-", nome, "-", autor)

    @classmethod
    def pesquisar_livro(cls, nome_livro):
        """
        Busca um registro específico utilizando a função LOWER para garantir a insensibilidade a maiúsculas.
        """
        # Uso de marcadores de parâmetro (?) para prevenir ataques de SQL Injection
        cls.cursor.execute("SELECT nome FROM Livros WHERE LOWER(nome) = LOWER(?)", (nome_livro,))

        # Recuperação de apenas uma linha de resultado (ou None)
        resultado = cls.cursor.fetchone()

        if resultado:
            print(f"Livro {resultado[0]} foi encontrado.")
        else:
            print("Livro não encontrado.")

    @classmethod
    def listar_livro_por_autor(cls, autor_desejado):
        """
        Filtra e retorna todos os registros associados a um autor específico.
        """
        cls.cursor.execute("SELECT nome, autor FROM Livros WHERE LOWER(autor) = LOWER(?)", (autor_desejado,))
        resultado = cls.cursor.fetchall()

        print(f"O autor {autor_desejado} possui {len(resultado)} livros:")
        if resultado:
            for nome, autor in resultado:
                print(nome, "-", autor)
        else:
            print("Este autor não possui livros.")

    @classmethod
    def remover_livro(cls, nome_livro):
        """
        Executa o comando DELETE no banco de dados. Requer commit para persistência.
        """
        cls.cursor.execute(
            "DELETE FROM Livros WHERE LOWER(nome) = LOWER(?)",
            (nome_livro,)
        )

        # Verifica a contagem de linhas afetadas para confirmar se a exclusão ocorreu
        if cls.cursor.rowcount > 0:
            cls.conexao.commit()  # Persiste a alteração no banco de dados
            print("Livro removido com sucesso.")
        else:
            print("Livro não encontrado.")

    # --- MÉTODOS DE ATUALIZAÇÃO (DML - DATA MANIPULATION LANGUAGE) ---

    @classmethod
    def atualizar_nome_livro(cls, id, nome_novo):
        """ Atualiza o campo 'nome' utilizando o identificador primário (ID). """
        cls.cursor.execute("UPDATE Livros SET nome = (?) WHERE id = (?)", (nome_novo, id))

        if cls.cursor.rowcount > 0:
            print("Operação realizada com sucesso.")
            cls.conexao.commit()
        else:
            print("Operação não realizada. Verifique o ID.")

    @classmethod
    def atualizar_autor_livro(cls, id, autor_novo):
        """ Valida se a entrada é uma string antes de proceder com o UPDATE. """
        if not autor_novo.isdigit():
            cls.cursor.execute("UPDATE Livros SET autor = (?) WHERE id = (?)", (autor_novo, id))
            if cls.cursor.rowcount > 0:
                print("Operação realizada com sucesso.")
                cls.conexao.commit()
        else:
            print("Operação inválida: O campo autor não deve conter apenas numerais.")

    @classmethod
    def atualizar_editora_livro(cls, id, editora_nova):
        """ Atualiza o campo 'editora' com validação de tipo de dado. """
        if not editora_nova.isdigit():
            cls.cursor.execute("UPDATE Livros SET editora = (?) WHERE id = (?)", (editora_nova, id))
            if cls.cursor.rowcount > 0:
                print("Operação realizada com sucesso.")
                cls.conexao.commit()
        else:
            print("Operação não realizada. Verifique os caracteres digitados.")

    @classmethod
    def atualizar_ano_lancamento_livro(cls, id, novo_ano_livro):
        """ Valida se a entrada do ano consiste exclusivamente em dígitos antes da persistência. """
        if novo_ano_livro.isdigit():
            cls.cursor.execute("UPDATE Livros SET ano = (?) WHERE id = (?)", (novo_ano_livro, id))
            if cls.cursor.rowcount > 0:
                print("Operação realizada com sucesso.")
                cls.conexao.commit()
        else:
            print("Operação negada: O ano de lançamento deve ser composto apenas por números.")

    @classmethod
    def atualizar_qtd_paginas_livro(cls, id, nova_qtd_paginas):
        """ Atualiza o campo 'paginas' garantindo a integridade do tipo de dado inteiro. """
        if nova_qtd_paginas.isdigit():
            cls.cursor.execute("UPDATE Livros SET paginas = (?) WHERE id = (?)", (nova_qtd_paginas, id))
            if cls.cursor.rowcount > 0:
                print("Operação realizada com sucesso.")
                cls.conexao.commit()
        else:
            print("Erro de validação: Verifique se foram digitados apenas números para a quantidade de páginas.")