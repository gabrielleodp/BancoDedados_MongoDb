# src/model/tarefa.py
class Tarefa:
    def __init__(self, id:int=None, titulo:str="", descricao:str="", status:str="PENDENTE", usuario_id:int=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.usuario_id = usuario_id

    def to_string(self):
        return f"ID: {self.id} | Título: {self.titulo} | Status: {self.status} | Usuário ID: {self.usuario_id}"
