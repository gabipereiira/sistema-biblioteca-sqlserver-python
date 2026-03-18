📚 Sistema de Gerenciamento de Biblioteca (Python + SQL Server)
Este projeto consiste em uma aplicação para o gerenciamento de uma bilioteca de livros, integrando Python 3 com o banco de dados Microsoft SQL Server. O foco principal foi a aplicação de conceitos de Orientação a Objetos (POO) e a Persistência de Dados em um ambiente de banco de dados relacional profissional.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.14

Banco de Dados: Microsoft SQL Server (17.0 RTM)

Biblioteca de Conexão: pyodbc

Ambiente de Desenvolvimento: PyCharm / SQL Server Management Studio (SSMS)

🏗️ Arquitetura do Projeto
O sistema foi dividido em três camadas principais para garantir a facilidade de manutenção:

banco.py (Infraestrutura): Responsável pela lógica de conexão, verificação de existência do database e provisionamento inicial.

livro.py (Regra de Negócio): Contém a classe Livro com métodos estáticos e de classe para operações DML (Data Manipulation Language).

main.py (Interface/Fluxo): Ponto de entrada da aplicação, gerencia o menu de interação com o usuário e a criação da tabela no banco de dados.

🚀 Funcionalidades (CRUD)
Create (Cadastrar): Inserção de novos livros com validação de tipos de dados (ex: páginas como inteiro).

Read (Listar/Pesquisar): * Exibição de todos os livros cadastrados com seus respectivos IDs.

Busca por título (Case Insensitive).

Exibição de obras filtradas por autor.

Update (Atualizar): Atualização de campos específicos (Nome, Autor, Ano, Editora, Páginas) utilizando o ID como chave primária.

Delete (Remover): Exclusão de registros com base no nome do livro.

🔒 Segurança e Integridade
Prevenção de SQL Injection: Utilização de consultas parametrizadas (?) em todos os comandos executados pelo cursor.

Validação de Entrada: Implementação de métodos como .isdigit() para garantir a integridade dos tipos de dados antes da persistência.

Gestão de Transações: Uso de conexao.commit() para garantir que as alterações sejam gravadas permanentemente apenas após o sucesso da operação.

📋 Como Executar
Certifique-se de ter o Microsoft SQL Server instalado e o serviço ativo.

Instale o driver ODBC e a biblioteca pyodbc:

pip install pyodbc

Configure a string de conexão no arquivo banco.py para apontar para o seu servidor local (localhost).

Execute o arquivo principal:

python main.py