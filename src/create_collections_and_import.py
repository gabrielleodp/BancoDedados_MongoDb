import logging
import json
from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries

LIST_OF_COLLECTIONS = ["usuarios", "tarefas"]

logger = logging.getLogger(name="C2_MongoDB_Import")
logger.setLevel(level=logging.WARNING)

mongo = MongoQueries()

def createCollections(drop_if_exists: bool = False):
    """
    Cria as coleções no MongoDB seguindo o edital.
    Caso drop_if_exists=True, apaga a coleção se já existir.
    """
    mongo.connect()
    existing = mongo.db.list_collection_names()

    for collection in LIST_OF_COLLECTIONS:
        if collection in existing:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} apagada!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} criada novamente!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} criada!")

    mongo.close()


def insert_many(data: json, collection: str):
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()


def extract_and_insert():
    """
    Extrai dados do Oracle e insere no MongoDB
    mantendo exatamente a estrutura da C2.
    """
    oracle = OracleQueries()
    oracle.connect()

    # Tabelas do seu projeto
    sql = "SELECT * FROM {table}"

    for collection in LIST_OF_COLLECTIONS:
        # Lê os dados do Oracle como DataFrame
        df = oracle.sqlToDataFrame(sql.format(table=collection.upper()))

        logger.warning(f"Dados extraídos de {collection.upper()} no Oracle")

        # Converte DataFrame em JSON
        records = json.loads(df.T.to_json()).values()
        logger.warning("Dados convertidos para JSON")

        # Inserir documentos no MongoDB
        insert_many(records, collection)
        logger.warning(f"Documentos inseridos na coleção {collection}")


if __name__ == "__main__":
    logging.warning("Iniciando processo de importação Oracle → MongoDB")
    createCollections(drop_if_exists=True)   # recriar coleções
    extract_and_insert()
    logging.warning("Processo finalizado")
