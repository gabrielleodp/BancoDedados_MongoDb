from src.conexion.oracle_queries import OracleQueries

class SplashScreen:

    def get_updated_screen(self):
        conn = OracleQueries()
        try:
            usuarios_count = conn.sqlToMatrix("SELECT COUNT(1) FROM usuarios")[0][0]
            tarefas_count = conn.sqlToMatrix("SELECT COUNT(1) FROM tarefas")[0][0]
        except:
            usuarios_count = 0
            tarefas_count = 0

        splash_text = (
            "===================================\n"
            "     Sistema de Gerenciamento de Tarefas\n"
            "     Grupo: Gabrielle, Adrielly, Luísa\n"
            "     Professor: Howard Cruz Roatti\n"
            "     Disciplina: Banco de Dados\n"
            "     Semestre: 2025/2\n"
            f"     Total de Usuários: {usuarios_count}\n"
            f"     Total de Tarefas: {tarefas_count}\n"
            "===================================\n"
        )
        return splash_text
