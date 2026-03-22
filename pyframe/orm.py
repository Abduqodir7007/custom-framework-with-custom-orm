import sqlite3
from typing import Self


class DataTypes:

    TYPE_MAP = {
        # strings
        str: "TEXT",
        # integers
        int: "INTEGER",
        # floating point
        float: "REAL",
        # boolean
        bool: "BOOLEAN",
        # binary data
        bytes: "BLOB",
        # None type (nullable handling)
        type(None): "NULL",
        # optional: custom handling later
    }


class Column:
    def __init__(self, py_type) -> None:
        self.py_type = py_type

    @property
    def sql_type(self):
        try:
            return DataTypes.TYPE_MAP[self.py_type]
        except KeyError:
            raise TypeError("Unsupported data type")


class Table:
    _db = None

    def __init__(self, **kwargs) -> None:
        for name, value in kwargs.items():
            setattr(self, name, value)

    @classmethod
    def get_table_name(cls) -> str:
        return str(cls.__name__).lower()

    @classmethod
    def _get_fields(cls) -> dict:
        columns = {}
        for name, value in cls.__dict__.items():
            if isinstance(value, Column):
                columns[name] = value
        return columns

    @classmethod
    def _build_columns_sql(cls) -> str:
        columns = cls._get_fields()
        parts = []

        for name, column in columns.items():
            parts.append(f"{name} {column.sql_type}")

        return ", ".join(parts)

    @classmethod
    def build_full_query(cls) -> str:

        parts = cls._build_columns_sql()
        table_name = cls.get_table_name()
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({parts})"
        except ValueError:
            raise TypeError("Table must have at least one column")
        return query

    def save(self) -> None:
        if self._db is None:
            raise TypeError("Please bind the database")

        table_name: str = self.__class__.get_table_name()
        columns: list = list(self.__class__._get_fields().keys())

        # print("table name: ", table_name)
        # print("column list: ", columns)

        column_names = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        values = tuple(getattr(self, col) for col in columns)

        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

        self.__class__._db.execute(query, values)

        return

    @classmethod
    def all(cls):
        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name}"

        res = cls._db.execute(query)
        return res.fetchall()

    @classmethod
    def get(cls, **kwargs):  # we can use kwargs to filter data with any fields
        table_name = cls.get_table_name()
        conditions = [f"{key} = ?" for key in kwargs]
        values = tuple(kwargs.values())

        query = f"SELECT * FROM {table_name} WHERE {" AND ".join(conditions)} LIMIT 1"
        res = cls._db.execute(query, values)
        return res.fetchall()

    def delete(self, **kwargs):
        pass

    def filter(self, **kwargs):
        pass


class Database:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name):
        if self._initialized:
            return

        self._initialized = True
        self.name = name

    def connection(self):
        return sqlite3.connect(self.name)

    def cursor(self):
        return self.connection().cursor()

    def execute(self, query, params=None):
        conn = self.connection()
        cursor = conn.cursor()
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()
        return cursor

    def create(self, model):
        model._db = self
        query = model.build_full_query()
        self.execute(query)

    def drop(self, model):
        model._db = self
        table_name = model.get_table_name()
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute(query)
