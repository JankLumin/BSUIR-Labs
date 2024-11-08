from psycopg2 import pool
import threading


class Database:
    _instance = None
    _lock = threading.Lock()

    def __init__(
        self,
        minconn=1,
        maxconn=10,
        dbname="mdsybd",
        user="postgres",
        password="8025",
        host="localhost",
        port="5432",
    ):
        try:
            self.pool = pool.SimpleConnectionPool(
                minconn,
                maxconn,
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
            )
            if not self.pool:
                raise Exception("Connection pool creation failed")
        except Exception as e:
            print(f"Error creating connection pool: {e}")
            raise e

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def execute(self, query, params=None, commit=False):
        conn = self.pool.getconn()
        result = None
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                else:
                    if cursor.description:
                        result = cursor.fetchall()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Error executing query: {e}")
            raise e
        finally:
            self.pool.putconn(conn)

    def call_procedure(self, procedure_name, *params):
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.callproc(procedure_name, params)
                results = None
                if cursor.description:
                    results = cursor.fetchall()
                conn.commit()
                return results
        except Exception as e:
            conn.rollback()
            print(f"Error calling procedure {procedure_name}: {e}")
            raise e
        finally:
            self.pool.putconn(conn)

    def close_all(self):
        self.pool.closeall()
