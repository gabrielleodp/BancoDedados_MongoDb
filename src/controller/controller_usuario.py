# src/controller/controller_usuario.py
from typing import List

class ControllerUsuario:
    def __init__(self, mongo):
        self.mongo = mongo  # instância de MongoQueries

    def inserir(self):
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        try:
            new_id = self.mongo.get_next_sequence("usuarios")
            doc = {"id_usuario": new_id, "nome": nome, "email": email}
            self.mongo.insert_one("usuarios", doc)
            print("Usuário inserido com sucesso!")
        except Exception as e:
            print("Erro ao inserir usuário:", e)

    def listar(self) -> List[int]:
        usuarios = self.mongo.find("usuarios", sort=[("id_usuario", 1)])
        for u in usuarios:
            print(f"{u.get('id_usuario')} - {u.get('nome')} ({u.get('email')})")
        return [u.get("id_usuario") for u in usuarios]

    def atualizar(self):
        usuarios = self.mongo.find("usuarios", sort=[("id_usuario", 1)])
        print("USUÁRIOS CADASTRADOS:")
        for u in usuarios:
            print(f"{u.get('id_usuario')} - {u.get('nome')} ({u.get('email')})")
        ids = [u.get("id_usuario") for u in usuarios]

        try:
            id_usuario = int(input("ID do usuário a atualizar: "))
            if id_usuario not in ids:
                print("ID inválido.")
                return
            nome = input("Novo nome: ").strip()
            email = input("Novo email: ").strip()
            res = self.mongo.update_one_by_field(
                "usuarios",
                "id_usuario",
                id_usuario,
                {"$set": {"nome": nome, "email": email}}
            )
            if res.modified_count > 0:
                print("Usuário atualizado com sucesso!")
            else:
                print("Nenhuma alteração detectada.")
        except Exception as e:
            print("Erro ao atualizar usuário:", e)

    def excluir(self):
        usuarios = self.listar()
        try:
            id_usuario = int(input("ID do usuário a excluir: "))
            if id_usuario not in usuarios:
                print("ID inválido.")
                return
            confirm = input("Deseja realmente excluir? (S/N): ").strip().upper()
            if confirm == "S":
                # verificar tarefas vinculadas
                tarefas = self.mongo.find("tarefas", {"usuario_id": id_usuario})
                if tarefas:
                    print("Não é possível excluir este usuário. Existem tarefas vinculadas a ele.")
                    resp = input("Deseja excluir também as tarefas vinculadas? (S/N): ").strip().upper()
                    if resp != "S":
                        return
                    # excluir tarefas filhas
                    for t in tarefas:
                        self.mongo.delete_one_by_field("tarefas", "id_tarefa", t.get("id_tarefa"))
                self.mongo.delete_one_by_field("usuarios", "id_usuario", id_usuario)
                print("Usuário excluído com sucesso!")
        except Exception as e:
            print("Erro ao excluir usuário:", e)
