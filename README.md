# Sistema de Gerenciamento de Tarefas em Python com Oracle

Este sistema foi desenvolvido como atividade acadêmica da disciplina de **Banco de Dados**.  
O projeto implementa um **sistema de gerenciamento de tarefas e usuários**, permitindo realizar operações CRUD (Create, Read, Update, Delete) integradas ao Banco de Dados Oracle.

O sistema foi construído utilizando o **padrão MVC (Model-View-Controller)**, com separação clara entre as camadas de modelo, controle e visualização.

- [Vídeo da execução](https://www.youtube.com/watch?v=8sFr8z8dwXo)

## É necessário já ter pré-instalado:
- Python 3.8 ou superior, verifique se já está instalado:
```bash
python --version
```
- Oracle ativo (local ou via container), verifique se já possui:
```bash
docker ps
```
- Instant Client do Oracle (para a biblioteca cx_Oracle), verifique se já possui:
```bash
echo $LD_LIBRARY_PATH
```
---

## Organização do Projeto

**diagrama:** contém o diagrama relacional representando as entidades e relacionamentos do sistema.  
O sistema possui as entidades: **USUÁRIOS** e **TAREFAS**.

---

**sql:** scripts SQL utilizados para criar as tabelas e inserir dados fictícios.  
- create_tables.sql → criação das tabelas e sequencias.  
- insert_tarefas.sql → inserção de registros de exemplo.  
- insert_usuarios.sql → inserção de registros de exemplo.  
- relatorio_group_by.sql → relatório agrupado por usuário
- relatorio_join.sql → relatório detalhado com JOIN

---

**src:** código-fonte do sistema.  
- conexion/ → módulo de conexão com o Oracle (oracle_queries.py).  
- controller/ → classes responsáveis por inserir, alterar e excluir registros.  
- model/ → classes que representam as entidades do sistema (Usuário e Tarefa).  
- reports/ → módulo relatorios.py responsável por gerar relatórios.  
- utils/ → scripts auxiliares, como config.py e splash_screen.py.  
- create_tables_and_records.py → cria tabelas e insere registros de exemplo.  

---

**config.py** → configurações globais do sistema.

**main.py** → ponto de entrada do sistema (menu principal no terminal).  

**requirements.txt** → dependências do projeto.

---

## Bibliotecas Utilizadas

**requirements.txt:**  
```bash
pip install -r requirements.txt
```
---

## Passo a passo para executar o projeto:

**1.	Baixar o projeto:**
- Clonar do GitHub ou baixar o zip e extrair.

**2.	Abrir o terminal na pasta do projeto:**
- Ex.: ~/ProjetoBancoDeDados

**3.	Criar um ambiente virtual (opcional, mas recomendado):**
```bash 
python3 -m venv venv_proj
```

depois ative o ambiente:
- (no Linux): 
```bash 
source venv_proj/bin/activate
```
- (no windows/cmd): 
```bash
venv_proj\Scripts\activate
```

**4.	Instalar as dependências:**
```bash 
pip install -r requirements.txt
```

**5.	Configurar conexão Oracle:**
- Certifique-se que o Oracle está rodando (ex.: via container)
- primeiro vá para o caminho do docker
```bash
cd /home/labdatabase/database_services
```
- Suba/inicie o Oracle:
```bash
docker compose up -d
```
- O arquivo src/conexion/passphrase/authentication.oracle já contém o usuário e senha.
- Não é necessário criar nada manualmente no DBeaver.

**6.	Criar as tabelas e inserir os dados de exemplo:**
- No terminal, volte para o caminho do projeto:
```bash
cd ~/ProjetoBancoDeDados
```
- Insira o comando: 
```bash
python create_tables_and_records.py
```

**7.	Rodar o programa:**
- No terminal, dentro do ambiente virtual e da pasta do projeto, que deve mostrar:

 (venv_proj) labdatabase@lab-database-class:~/ProjetoBancoDeDados$ 
- Digite: 
```bash
python main.py
```

**8.	Usar o sistema:**
- Siga os menus no terminal para inserir usuários ou tarefas, excluir/atualizar dados, consultar registros e gerar relatórios.

**9.	Encerrar:**
- Digite a opção de sair no menu principal.
- Se estiver usando ambiente virtual, desative-o digitando: 
```bash
deactivate
```

---

## Funcionalidades Principais

### Usuários
- Inserir usuário  
- Atualizar usuário  
- Excluir usuário 
- Listar usuários  

### Tarefas
- Inserir tarefa  
- Atualizar tarefa  
- Excluir tarefa  
- Listar tarefas  

### Relatórios
- **Relatório de Tarefas por Usuário (GROUP BY)**  
- **Relatório Detalhado de Tarefas (JOIN)** 

__________________________________

## Contagem de Registros

Ao iniciar o sistema, são exibidos:
- O total de **usuários cadastrados**  
- O total de **tarefas cadastradas**
____________________________________

## Grupo
- Adrielly Costa
- Gabrielle Oliveira de Paula
- Luísa Vernersbach Varejão

**Professor:** Howard
**Disciplina:** Banco de Dados  
**Semestre:** 2025/2
