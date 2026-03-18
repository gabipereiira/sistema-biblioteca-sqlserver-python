import pyodbc


def conectar():
    """
    Estabelece a conexão inicial com o servidor e garante a existência do banco de dados.
    Utiliza o driver ODBC 18 para SQL Server.
    """

    # Primeira conexão: Aponta para o banco 'master' (sistema) para realizar tarefas administrativas.
    # O parâmetro 'autocommit=True' permite a execução de comandos DDL (como CREATE DATABASE).
    conexao = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=master;"
        "TrustServerCertificate=yes;"
        "Encrypt=no;"
        "Trusted_connection=yes;",
        autocommit=True
    )

    # Instanciação do objeto cursor para execução de comandos SQL.
    cursor = conexao.cursor()

    # Bloco de verificação de existência do Banco de Dados.
    # Consulta a tabela de sistema 'sys.databases' para evitar erro de duplicidade na criação.
    cursor.execute("""
    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'DB_biblioteca')
    CREATE DATABASE DB_biblioteca
    """)

    # Encerramento dos objetos de comunicação com o banco 'master'.
    # É uma boa prática de gestão de recursos fechar a conexão antes de abrir uma nova.
    conexao.commit()
    cursor.close()
    conexao.close()

    # Segunda conexão: Retorna o objeto de conexão apontando especificamente para 'DB_biblioteca'.
    # Este objeto será utilizado pelas outras classes para manipulação de dados (DML).
    return pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=DB_biblioteca;"
        "TrustServerCertificate=yes;"
        "Encrypt=no;"
        "Trusted_connection=yes;"
    )