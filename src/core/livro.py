import pyodbc


class Livro:
    # Atributos de classe que armazenarão a instância de conexão e o cursor do banco de dados
    cursor = None
    conexao = None

    def __init__(self, nome, autor, ano=None,editora=None,paginas=None):
        """
        Método construtor da classe Livro.
        :param nome: String representando o título do livro.
        :param autor: String representando o autor do livro.
        :param extras: Dicionário de argumentos variáveis para atributos opcionais.
        """
        self.nome = nome
        self.autor = autor
        self.ano = ano
        self.editora = editora
        self.paginas = paginas

    def adicionar_livro(self):
        sql = "INSERT INTO Livros ( nome, autor, ano, editora, paginas) VALUES (?, ?, ?, ?, ?)"
        # O self acessa os dados que o __init__ guardou
        valores = (self.nome, self.autor, self.ano, self.editora, self.paginas)
        self.cursor.execute(sql, valores)
        self.conexao.commit()
    @classmethod
    def mostrar_biblioteca(cls):
        """
        Realiza uma consulta de seleção (SELECT) para listar os 10 primeiros registros da tabela Livros.
        """
        # Execução da query SQL solicitando colunas específicas para otimização de performance
        cls.cursor.execute("SELECT TOP 10 id, nome, autor FROM Livros ORDER BY id")
        # Pega os nomes das colunas (id, nome, autor) automaticamente
        # Isso evita que você tenha que digitar linha[0], linha[1]..
        resultados = [coluna[0] for coluna in cls.cursor.description]
        # Transforma cada linha em um dicionário
        #zip (colunas, linhas) junta o nome da coluna com o valor dela
        livros = cls.cursor.fetchall()
        livros_dic = [dict(zip(resultados,linha)) for linha in livros]
        return livros_dic

    @classmethod
    def pesquisar_livro(cls, nome_livro):
        """
        Busca um registro específico utilizando a função LOWER para garantir a insensibilidade a maiúsculas.
        """
        #Adicionamos os símbolos '%' para o SQL buscar o texto em qualquer parte do nome (Busca Parcial)
        busca = f"%{nome_livro}%"
        # Uso de marcadores de parâmetro (?) para prevenir ataques de SQL Injection
        cls.cursor.execute("SELECT id, nome FROM Livros WHERE nome LIKE (?)", (busca,))
        # Recuperação de resultados da consulta
        resultados = [coluna[0] for coluna in cls.cursor.description]
        # zip (colunas, linhas) junta o nome da coluna com o valor dela
        livros_encontrados = cls.cursor.fetchall()
        if livros_encontrados:
            print(f"Livro {resultados[0]} foi encontrado.")
        else:
            print("Livro não encontrado.")
        livros_dic = [dict(zip(resultados, linha)) for linha in livros_encontrados]
        return livros_dic
    @classmethod
    def remover_livro(cls, id_livro):
        """
        Executa o comando DELETE no banco de dados. Requer commit para persistência.
        """
        cls.cursor.execute(
            "DELETE FROM Livros WHERE id = ?",
            (id_livro,)
        )
        linhas_afetadas = cls.cursor.rowcount
        # Verifica a contagem de linhas afetadas para confirmar se a exclusão ocorreu
        if linhas_afetadas > 0:
            cls.conexao.commit()  # Persiste a alteração no banco de dados
            print("Livro removido com sucesso.")
        else:
            print("Livro não encontrado.")
        return linhas_afetadas
    # --- MÉTODOS DE ATUALIZAÇÃO (DML - DATA MANIPULATION LANGUAGE) ---
    @classmethod
    def atualizar_livro(cls,id_livro,nome=None,autor=None,editora=None,paginas=None,ano=None):
    # Atualiza todos os dados de um livro de uma vez só usando o ID
        cls.cursor.execute("""
            UPDATE Livros
            SET nome = COALESCE(?,nome),
            autor = COALESCE(?,autor),
            ano = COALESCE(?,ano),
            editora = COALESCE(?,editora),
            paginas = COALESCE(?,paginas)
        WHERE id = ?
    """,(nome,autor,ano,editora,paginas,id_livro))
        linhas_afetadas = cls.cursor.rowcount
        if linhas_afetadas > 0:
            cls.conexao.commit()
            return{"mensagem":"Livro Atualizado com Suceso"}
        else:
            return{"mensagem":"Livro com o ID informado nao foi encontrado."}
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
