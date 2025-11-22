from src.conexion.oracle_queries import OracleQueries
import os

def execute_commands(commands, oracle: OracleQueries, is_write=True):
    """Executa uma lista de comandos SQL no Oracle"""
    for command in commands:
        cmd = command.strip()
        if not cmd:
            continue
        try:
            if is_write:
                oracle.write(cmd)
            else:
                oracle.executeDDL(cmd)
            print(f"Executado: {cmd[:50]}{'...' if len(cmd) > 50 else ''}")
        except Exception as e:
            print(f"Erro ao executar comando: {cmd[:50]}... \n{e}")

def read_sql_file(path):
    """Lê um arquivo .sql e retorna uma lista de comandos separados por ;"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return [cmd.strip() for cmd in content.split(";") if cmd.strip()]

def drop_tables(oracle: OracleQueries):
    """Tenta remover tabelas caso existam"""
    tables = ["TAREFAS", "USUARIOS"]
    for table in tables:
        try:
            oracle.executeDDL(f"DROP TABLE {table} CASCADE CONSTRAINTS")
            print(f"Tabela {table} removida (se existia).")
        except Exception as e:
            print(f"Não foi possível remover {table}: {e}")

def run():
    oracle = OracleQueries(can_write=True)
    oracle.connect()

    # 1️⃣ Remover tabelas antigas
    drop_tables(oracle)

    # 2️⃣ Criar tabelas
    sql_create_path = os.path.join("sql", "create_tables.sql")
    print("Criando tabelas...")
    create_commands = read_sql_file(sql_create_path)
    execute_commands(create_commands, oracle, is_write=False)
    print("Tabelas criadas com sucesso!\n")

    # 3️⃣ Inserir usuários
    sql_insert_usuarios = os.path.join("sql", "insert_usuarios.sql")
    print("Inserindo usuários...")
    insert_user_commands = read_sql_file(sql_insert_usuarios)
    execute_commands(insert_user_commands, oracle)
    print("Usuários inseridos com sucesso!\n")

    # 4️⃣ Inserir tarefas
    sql_insert_tarefas = os.path.join("sql", "insert_tarefas.sql")
    print("Inserindo tarefas...")
    insert_task_commands = read_sql_file(sql_insert_tarefas)
    execute_commands(insert_task_commands, oracle)
    print("Tarefas inseridas com sucesso!\n")

    # 5️⃣ Consultas de teste
    total_usuarios = oracle.read("SELECT COUNT(1) FROM USUARIOS")[0][0]
    total_tarefas = oracle.read("SELECT COUNT(1) FROM TAREFAS")[0][0]
    print(f"Total de usuários: {total_usuarios}")
    print(f"Total de tarefas: {total_tarefas}\n")

    # 6️⃣ Executar relatórios
    print("RELATÓRIOS AUTOMÁTICOS:")

    # Relatório GROUP BY
    sql_group_by = os.path.join("sql", "relatorio_group_by.sql")
    group_commands = read_sql_file(sql_group_by)
    print("\n--- Relatório GROUP BY ---")
    for cmd in group_commands:
        result = oracle.read(cmd)
        for row in result:
            print(row)

    # Relatório JOIN
    sql_join = os.path.join("sql", "relatorio_join.sql")
    join_commands = read_sql_file(sql_join)
    print("\n--- Relatório JOIN ---")
    for cmd in join_commands:
        result = oracle.read(cmd)
        for row in result:
            print(row)

if __name__ == "__main__":
    run()

