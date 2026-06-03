import pyodbc
from sqlalchemy import create_engine

def conectar():
    # --- PRIMEIRA PARTE: GARANTE O BANCO (MASTER) ---
    conexao = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=master;"
        "TrustServerCertificate=yes;"
        "Encrypt=no;"
        "Trusted_connection=yes;",
        autocommit=True
    )
    cursor = conexao.cursor()
    cursor.execute("""
    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'DB_biblioteca')
    CREATE DATABASE DB_biblioteca
    """)
    cursor.close()
    conexao.close()

    # --- SEGUNDA PARTE: GARANTE A TABELA (DB_BIBLIOTECA) ---
    # Criação da conexão final e guardamos na variável 'conexao_final'
    conexao_final = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=DB_biblioteca;"
        "TrustServerCertificate=yes;"
        "Encrypt=no;"
        "Trusted_connection=yes;"
    )

    # Criação um cursor para esta conexão específica
    cursor_final = conexao_final.cursor()

    # Executamos a criação de tabela aqui
    cursor_final.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Livros' and xtype='U')
    CREATE TABLE Livros (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nome VARCHAR(MAX),
        autor VARCHAR(MAX),
        ano VARCHAR(20),
        editora VARCHAR(MAX),
        paginas INT
    )
    """)

    # IMPORTANTE:Commit para salvar e fechar a conexão
    conexao_final.commit()
    cursor_final.close()

    # Agora sim, retornamos a conexão pronta
    return conexao_final

#Função para conectar o alchemy ao SQL Server
def conectar_alchemy():
    conexao_alchemy = (
        "mssql+pyodbc://@localhost/DB_biblioteca?"
        "driver=ODBC+Driver+18+for+SQL+Server&"
        "trusted_connection=yes&"
        "Encrypt=no&"
        "TrustServerCertificate=yes"
    )
    return create_engine(conexao_alchemy)
