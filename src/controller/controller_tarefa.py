# src/controller/controller_tarefa.py
class ControllerTarefa:
    def __init__(self, mongo):
        self.mongo = mongo

    def inserir(self):
        titulo = input("Título da tarefa: ").strip()
        descricao = input("Descrição: ").strip()
        status = input("Status [PENDENTE/EM ANDAMENTO/CONCLUÍDO]: ").strip().upper()

        usuarios = self.mongo.find("usuarios", sort=[("id_usuario", 1)])
        print("Usuários disponíveis:")
        for u in usuarios:
            print(f"{u.get('id_usuario')} - {u.get('nome')}")

        usuario_id = int(input("ID do usuário responsável: "))
        try:
            new_id = self.mongo.get_next_sequence("tarefas")
            doc = {
                "id_tarefa": new_id,
                "titulo": titulo,
                "descricao": descricao,
                "status": status or "PENDENTE",
                "usuario_id": usuario_id
            }
            self.mongo.insert_one("tarefas", doc)
            print("Tarefa inserida com sucesso!")
        except Exception as e:
            print("Erro ao inserir tarefa:", e)

    def listar(self):
        tarefas = self.mongo.find("tarefas", sort=[("id_tarefa", 1)])
        for t in tarefas:
            print(f"{t.get('id_tarefa')} - {t.get('titulo')} ({t.get('status')})")
        return [t.get("id_tarefa") for t in tarefas]

    def atualizar(self):
        tarefas = self.mongo.aggregate("tarefas", [
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
        ])
        print("TAREFAS CADASTRADAS:")
        for t in tarefas:
            nome = t.get("usuario", {}).get("nome") if isinstance(t.get("usuario"), dict) else (t.get("usuario") or {}).get("nome")
            # depending on lookup result structure:
            if isinstance(t.get("usuario"), list) and len(t.get("usuario"))>0:
                nome = t["usuario"][0].get("nome")
            print(f"{t.get('id_tarefa')} - {t.get('titulo')} ({t.get('status')}) - Usuário: {nome}")
        ids = [t.get("id_tarefa") for t in tarefas]

        try:
            id_tarefa = int(input("ID da tarefa a atualizar: "))
            if id_tarefa not in ids:
                print("ID inválido.")
                return
            titulo = input("Novo título: ").strip()
            descricao = input("Nova descrição: ").strip()
            status = input("Novo status: ").strip().upper()

            usuarios = self.mongo.find("usuarios", sort=[("id_usuario", 1)])
            print("Usuários disponíveis:")
            for u in usuarios:
                print(f"{u.get('id_usuario')} - {u.get('nome')}")
            usuario_id = int(input("Novo ID do usuário responsável: "))

            res = self.mongo.update_one_by_field(
                "tarefas",
                "id_tarefa",
                id_tarefa,
                {"$set": {"titulo": titulo, "descricao": descricao, "status": status, "usuario_id": usuario_id}}
            )
            if res.modified_count > 0:
                print("Tarefa atualizada com sucesso!")
            else:
                print("Nenhuma alteração detectada.")
        except Exception as e:
            print("Erro ao atualizar tarefa:", e)

    def excluir(self):
        ids = self.listar()
        try:
            id_tarefa = int(input("ID da tarefa a excluir: "))
            if id_tarefa not in ids:
                print("ID inválido.")
                return
            confirm = input("Deseja realmente excluir? (S/N): ").strip().upper()
            if confirm == "S":
                self.mongo.delete_one_by_field("tarefas", "id_tarefa", id_tarefa)
                print("Tarefa excluída com sucesso!")
        except Exception as e:
            print("Erro ao excluir tarefa:", e)
