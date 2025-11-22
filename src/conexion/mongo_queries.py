# src/conexion/mongo_queries.py
import json
import os
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import PyMongoError
from pandas import DataFrame

class MongoQueries:
    """
    Wrapper simples para operações básicas do MongoDB.
    Substitui OracleQueries no projeto (mesmas responsabilidades principais).
    Mantém IDs numéricos através de uma coleção 'counters' (padrão Mongo).
    """

    def __init__(self, can_write: bool = False):
        self.can_write = can_write
        # padrão localhost; se houver arquivo de autenticação, tenta ler URI
        self.mongo_uri = "mongodb://localhost:27017"
        self.db_name = "labdatabase"

        auth_path = "src/conexion/passphrase/authentication.mongo"
        if os.path.exists(auth_path):
            with open(auth_path, "r") as f:
                # arquivo pode conter: mongodb://user:pass@host:port,labdatabase
                content = f.read().strip()
                if ',' in content:
                    uri, dbn = content.split(',', 1)
                    self.mongo_uri = uri.strip()
                    self.db_name = dbn.strip()
                else:
                    self.mongo_uri = content

        self.client = None
        self.db = None

    def connect(self):
        """Conecta e retorna o objeto db"""
        if not self.client:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
        return self.db

    def close(self):
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
            self.client = None
            self.db = None

    # ---------- Sequences / counters ----------
    def get_next_sequence(self, name: str) -> int:
        """
        Simula sequence com a coleção 'counters'. Retorna próximo valor inteiro.
        name: por exemplo 'usuarios' ou 'tarefas'
        """
        db = self.connect()
        try:
            doc = db.counters.find_one_and_update(
                {"_id": name},
                {"$inc": {"seq": 1}},
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            return int(doc["seq"])
        except PyMongoError as e:
            raise RuntimeError("Erro ao obter sequência: " + str(e))

    # ---------- CRUD básico ----------
    def insert_one(self, collection: str, document: dict):
        if not self.can_write:
            raise PermissionError("Escrita não permitida")
        db = self.connect()
        return db[collection].insert_one(document)

    def find(self, collection: str, filter: dict = None, projection: dict = None, sort: list = None):
        db = self.connect()
        cursor = db[collection].find(filter or {}, projection)
        if sort:
            cursor = cursor.sort(sort)
        return list(cursor)

    def find_one(self, collection: str, filter: dict = None, projection: dict = None):
        db = self.connect()
        return db[collection].find_one(filter or {}, projection)

    def update_one_by_field(self, collection: str, field: str, value, update_doc: dict):
        if not self.can_write:
            raise PermissionError("Escrita não permitida")
        db = self.connect()
        return db[collection].update_one({field: value}, update_doc)

    def delete_one_by_field(self, collection: str, field: str, value):
        if not self.can_write:
            raise PermissionError("Escrita não permitida")
        db = self.connect()
        return db[collection].delete_one({field: value})

    def aggregate(self, collection: str, pipeline: list):
        db = self.connect()
        return list(db[collection].aggregate(pipeline))

    def count(self, collection: str, filter: dict = None) -> int:
        db = self.connect()
        return db[collection].count_documents(filter or {})

    # ---------- Helpers para compatibilidade com partes que usavam DataFrame/json ----------
    def sqlToDataFrame(self, unused_query: str) -> DataFrame:
        # não usado diretamente; mantém assinatura apenas por compatibilidade mínima
        raise NotImplementedError("Use métodos do MongoQueries (find, aggregate, etc.)")

    def sqlToJson(self, unused_query: str):
        raise NotImplementedError("Use métodos do MongoQueries (find, aggregate, etc.)")
