# src/reports/relatorios.py
from src.conexion.mongo_queries import MongoQueries

class Relatorio:
    def __init__(self, mongo: MongoQueries):
        self.mongo = mongo

    def rel_usuarios(self):
        resultado = self.mongo.find("usuarios", sort=[("id_usuario", 1)])
        print("\nUSUÁRIOS CADASTRADOS:")
        print("-" * 40)
        for row in resultado:
            print(f"ID: {row.get('id_usuario')} | Nome: {row.get('nome')} | Email: {row.get('email')}")
        print("-" * 40)

    def rel_tarefas(self):
        pipeline = [
            {"$lookup": {
                "from": "usuarios",
                "localField": "usuario_id",
                "foreignField": "id_usuario",
                "as": "usuario"
            }},
            {"$unwind": {"path": "$usuario", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "id_tarefa": 1, "titulo": 1, "status": 1, "usuario.nome": 1
            }},
            {"$sort": {"id_tarefa": 1}}
        ]
        resultado = self.mongo.aggregate("tarefas", pipeline)
        print("\nTAREFAS CADASTRADAS:")
        print("-" * 50)
        for row in resultado:
            usuario = row.get("usuario")
            nome = usuario.get("nome") if isinstance(usuario, dict) else (usuario[0].get("nome") if isinstance(usuario, list) and len(usuario)>0 else None)
            print(f"ID: {row.get('id_tarefa')} | Título: {row.get('titulo')} | Status: {row.get('status')} | Responsável: {nome}")
        print("-" * 50)

    def rel_tarefas_group_by(self):
        pipeline = [
            {"$group": {"_id": "$usuario_id", "total_tarefas": {"$sum": 1}}},
            {"$lookup": {"from": "usuarios", "localField": "_id", "foreignField": "id_usuario", "as": "usuario"}},
            {"$unwind": {"path": "$usuario", "preserveNullAndEmptyArrays": True}},
            {"$project": {"usuario_nome": "$usuario.nome", "total_tarefas": 1}},
            {"$sort": {"total_tarefas": -1}}
        ]
        resultado = self.mongo.aggregate("tarefas", pipeline)
        print("\nTOTAL DE TAREFAS POR USUÁRIO:")
        print("-" * 40)
        for row in resultado:
            print(f"Usuário: {row.get('usuario_nome')} | Total de Tarefas: {row.get('total_tarefas')}")
        print("-" * 40)

    def rel_tarefas_join(self):
        # Mesmo que rel_tarefas (JOIN)
        self.rel_tarefas()

