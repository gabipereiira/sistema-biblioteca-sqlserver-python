from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from livro import Livro
from banco import conectar

# Configuração inicial da API da Biblioteca
app = FastAPI(title="Biblioteca API v1.0")

# Gerenciamento da conexão com o Banco de Dados (SQL Server)
# Compartilhamos a conexão e o cursor com a classe Livro para operações de CRUD
conexao = conectar()
cursor = conexao.cursor()
Livro.conexao = conexao
Livro.cursor = cursor


# Schema para criação de livros (Validação de entrada)
class LivroBase(BaseModel):
    id: Optional[int] = None
    nome: str
    autor: str
    ano: Optional[int] = None
    editora: Optional[str] = None
    paginas: Optional[int] = None


# Schema para atualização de dados (Permite campos opcionais)
class LivroUpdate(BaseModel):
    nome: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    editora: Optional[str] = None
    paginas: Optional[int] = None


# Endpoint POST: Realiza o cadastro de um novo livro no sistema
@app.post("/adicionar-livro", status_code=status.HTTP_201_CREATED)
def adicionar_livro(livro: LivroBase):
    try:
        novo_livro = Livro(
            nome=livro.nome,
            autor=livro.autor,
            ano=livro.ano,
            editora=livro.editora,
            paginas=livro.paginas
        )
        novo_livro.adicionar_livro()
        return {"mensagem": f"Livro '{livro.nome}' cadastrado com sucesso."}
    except Exception as Erro:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar o cadastro: {Erro}"
        )


# Endpoint GET: Recupera todos os registros da biblioteca
@app.get("/mostrar-biblioteca", status_code=status.HTTP_200_OK)
def mostrar_biblioteca():
    try:
        resultado = Livro.mostrar_biblioteca()
        return resultado
    except Exception as Erro:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Erro ao consultar o acervo: {Erro}"
        )


# Endpoint GET: Busca livros por termo de pesquisa (nome ou autor)
@app.get("/pesquisar-livro", status_code=status.HTTP_200_OK)
def pesquisar_livro(livro_pesquisado: str):
    try:
        resultados = Livro.pesquisar_livro(livro_pesquisado)
        if not resultados:
            return {"mensagem": "Nenhum registro encontrado para esta busca."}
        return {
            "mensagem": "Busca concluída com sucesso!",
            "dados": resultados
        }
    except Exception as Erro:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao localizar o livro: {Erro}"
        )


# Endpoint PUT: Atualiza informações de um livro específico via ID
@app.put("/atualizar-livro/{id_livro}", status_code=status.HTTP_200_OK)
def atualizacao_livro(id_livro: int, livro_dados: LivroUpdate):
    try:
        # Converte os dados recebidos em dicionário, ignorando campos não enviados (nulls)
        dados_atualizados = livro_dados.dict(exclude_unset=True)
        resultado = Livro.atualizar_livro(id_livro, **dados_atualizados)

        if resultado == 0:
            return {"mensagem": "Livro não localizado no banco de dados."}

        return {"mensagem": "Cadastro atualizado com sucesso."}
    except Exception as Erro:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Erro na atualização. Certifique-se de enviar dados válidos."
        )


# Endpoint DELETE: Remove permanentemente um livro pelo ID
@app.delete("/deletar-livro/{id_livro}", status_code=status.HTTP_200_OK)
def excluir_livro(id_livro: int):
    try:
        resultado = Livro.remover_livro(id_livro)
        if resultado > 0:
            return {"mensagem": "Registro removido com sucesso."}
        else:
            return {"mensagem": "Livro não encontrado para exclusão."}
    except Exception as Erro:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao tentar excluir o registro: {Erro}"
        )