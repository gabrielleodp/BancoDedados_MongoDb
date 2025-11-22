# src/utils/splash_screen.py
from src.conexion.mongo_queries import MongoQueries

class SplashScreen:

    def get_updated_screen(self):
        conn = MongoQueries()
        try:
            usuarios_count = conn.count("usuarios")
            tarefas_count = conn.count("tarefas")
        except:
            usuarios_count = 0
            tarefas_count = 0

        splash_text = (
            "===========================================================\n"
            "   📝 SISTEMA DE GERENCIAMENTO DE TAREFAS\n"
            "   👥 Grupo: Adrielly Costa, Gabrielle Oliveira e Luísa Varejão\n"
            "   💻 Professor: Howard Cruz Roatti\n"
            "   📒 Disciplina: Banco de Dados\n"
            "   📅 Semestre: 2025/2\n"
            f"   👤 Total de Usuários: {usuarios_count}\n"
            f"   📝 Total de Tarefas: {tarefas_count}\n"
            "===========================================================\n"
        )
        return splash_text
