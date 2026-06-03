# Sistema de Gerenciamento de Biblioteca

Aplicação desenvolvida em Python com SQL Server para cadastro e gerenciamento de livros.  
O projeto foi criado com foco em Programação Orientada a Objetos (POO), persistência de dados e uso de banco relacional.

## Tecnologias utilizadas

- Python 3.14
- Microsoft SQL Server 17.0 RTM
- pyodbc
- PyCharm
- SQL Server Management Studio (SSMS)

## Estrutura do projeto

- `banco.py`: responsável pela conexão com o banco, verificação da existência do database e provisionamento inicial.
- `livro.py`: contém a classe `Livro` e os métodos relacionados às operações de banco.
- `main.py`: ponto de entrada da aplicação, com o menu principal e a criação da tabela.

## Funcionalidades

### Frontend da API
- Adicionar livros.
- Buscar livros.

### Versão em terminal
- Cadastrar livros.
- Listar todos os livros cadastrados.
- Buscar livros por título, com pesquisa case insensitive.
- Filtrar livros por autor.
- Atualizar livros usando o ID como chave primária.
- Excluir livros pelo nome.

## Segurança e integridade

- Uso de consultas parametrizadas para evitar SQL Injection.
- Validação de entrada com `isdigit()` para campos numéricos.
- Uso de `commit()` para confirmar alterações no banco de dados.

## Como executar

1. Certifique-se de ter o Microsoft SQL Server instalado e em execução.
2. Instale a biblioteca de conexão:

```bash
pip install pyodbc
```

3. Configure a string de conexão no arquivo `banco.py`.
4. Execute a aplicação:

```bash
python main.py
```

## Observações

- O frontend da API ainda não contempla todas as funcionalidades disponíveis no terminal.
- O projeto foi desenvolvido com fins de estudo e prática de POO com banco de dados relacional.
