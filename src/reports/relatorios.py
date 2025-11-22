from src.conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self, oracle: OracleQueries):
        self.oracle = oracle  # usa a conexão existente

    def rel_usuarios(self):
        resultado, _ = self.oracle.sqlToMatrix("SELECT id_usuario, nome, email FROM usuarios")
        print("USUÁRIOS CADASTRADOS:")
        for row in resultado:
            print(row)

    def rel_tarefas(self):
        resultado, _ = self.oracle.sqlToMatrix("""
            SELECT t.id_tarefa, t.titulo, t.status, u.nome
            FROM tarefas t
            JOIN usuarios u ON t.usuario_tarefa = u.id_usuario
        """)
        print("TAREFAS CADASTRADAS:")
        for row in resultado:
            print(row)

    def rel_tarefas_group_by(self):
        resultado, _ = self.oracle.sqlToMatrix(
            "SELECT usuario_tarefa, COUNT(*) AS total_tarefas FROM tarefas GROUP BY usuario_tarefa"
        )
        print("TOTAL DE TAREFAS POR USUÁRIO:")
        for row in resultado:
            print(row)

    def rel_tarefas_join(self):
        resultado, _ = self.oracle.sqlToMatrix("""
            SELECT t.id_tarefa, t.titulo, t.status, u.nome
            FROM tarefas t
            JOIN usuarios u ON t.usuario_tarefa = u.id_usuario
        """)
        print("TAREFAS COM DADOS DO USUÁRIO (JOIN):")
        for row in resultado:
            print(row)

