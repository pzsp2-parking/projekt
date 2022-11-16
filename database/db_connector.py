from threading import Lock
import mysql.connector


class SingletonMeta(type):
    """
    Thread-safe implementation of Singleton.
    """

    _instances = {}
    _lock: Lock = Lock()


    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DBConn(metaclass=SingletonMeta):
    host: str = "localhost"
    user="pzsp2"
    password="parking" # parking_pzsp2
    database="parpa"

    def __init__(self):
        self.db_connection=mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
            )
        self.db_cur = self.db_connection.cursor()
    
    def get_cur(self):
        return self.db_cur

    def execute(self, path):
        stmts = []
        stmt = ""
        with open(path) as fp:
            for line in fp.readlines():
                line = line.replace('\n', '')
                if not line:
                    continue
                if line[-1]==';':
                    stmt+=line
                    stmts.append(stmt)
                    stmt=""
                    continue
                stmt+=line
        for stmt in stmts:
            self.db_cur.execute(stmt)
        self.db_connection.commit()


db_cur=DBConn().get_cur()


# https://refactoring.guru/design-patterns/singleton/python/example#example-1
