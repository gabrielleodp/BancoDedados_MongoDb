# src/model/usuario.py
class Usuario:
    def __init__(self, id:int=None, nome:str="", email:str=""):
        self.id = id
        self.nome = nome
        self.email = email

    def to_string(self):
        return f"ID: {self.id} | Nome: {self.nome} | Email: {self.email}"
