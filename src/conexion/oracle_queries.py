import json
import cx_Oracle
from pandas import DataFrame

class OracleQueries:

    def __init__(self, can_write: bool = False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = 'XEPDB1'

        # Lê usuário e senha do arquivo
        with open("src/conexion/passphrase/authentication.oracle", "r") as f:
            self.user, self.passwd = f.read().strip().split(',')

        self.conn = None
        self.cur = None

    def __del__(self):
        # Fecha a conexão se existir, ignorando erro de interface
        try:
            if self.cur:
                self.close()
        except cx_Oracle.InterfaceError:
            pass

    def connectionString(self):
        """
        Cria a string de conexão usando service_name
        """
        return cx_Oracle.makedsn(
            host=self.host,
            port=self.port,
            service_name=self.service_name
        )

    def connect(self):
        """
        Conecta ao banco Oracle e retorna o cursor
        """
        self.conn = cx_Oracle.connect(
            user=self.user,
            password=self.passwd,
            dsn=self.connectionString()
        )
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query: str) -> DataFrame:
        """
        Executa query e retorna DataFrame
        """
        cur = self.connect()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            return DataFrame(rows, columns=[col[0].lower() for col in cur.description])
        finally:
            self.close()

    def sqlToMatrix(self, query: str):
        """
        Executa query e retorna matriz + nomes de colunas
        """
        cur = self.connect()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            matrix = [list(row) for row in rows]
            columns = [col[0].lower() for col in cur.description]
            return matrix, columns
        finally:
            self.close()

    def sqlToJson(self, query: str):
        """
        Executa query e retorna JSON
        """
        cur = self.connect()
        try:
            cur.execute(query)
            columns = [col[0].lower() for col in cur.description]
            cur.rowfactory = lambda *args: dict(zip(columns, args))
            rows = cur.fetchall()
            return json.dumps(rows, default=str)
        finally:
            self.close()

    def write(self, query: str):
        """
        Executa query de escrita (INSERT, UPDATE, DELETE)
        """
        if not self.can_write:
            raise PermissionError("Escrita não permitida")

        cur = self.connect()
        try:
            cur.execute(query)
            self.conn.commit()
        finally:
            self.close()

    def close(self):
        """
        Fecha cursor e conexão
        """
        if self.cur:
            try:
                self.cur.close()
            except cx_Oracle.InterfaceError:
                pass
            self.cur = None
        if self.conn:
            try:
                self.conn.close()
            except cx_Oracle.InterfaceError:
                pass
            self.conn = None

    def executeDDL(self, query: str):
        """
        Executa comando DDL (CREATE TABLE, SEQUENCE etc.)
        """
        cur = self.connect()
        try:
            cur.execute(query)
            self.conn.commit()
        finally:
            self.close()

