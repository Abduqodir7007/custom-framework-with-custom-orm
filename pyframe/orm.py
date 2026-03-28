import sqlite3
from typing import Self, Tuple


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


class Query:
    def __init__(self, model) -> None:
        self.model = model
        self.filters = []
        self.selected_fields = None

    def all(self):
        table_name = self.model.__name__
        query = f"SELECT * FROM {table_name}"

        res = self.model._db.execute(query)
        return res.fetchall()

    def get(self, **kwargs):
        if not kwargs:
            raise Exception("Cannot use get without key word arguments")

        table_name = self.model.__name__
        conditions = [f"{key} = ?" for key in kwargs]
        where_clause = " AND ".join(conditions)
        values = tuple(kwargs.values())

        query = f"SELECT * FROM {table_name} WHERE {where_clause}"
        res = self.model._db.execute(query, values)
        data = res.fetchall()

        if len(data) == 0:
            raise Exception("Object does not exists")

        if len(data) > 1:
            raise Exception("Multiple Object exists")

        return data[0]

    def delete(self, **kwargs):
        table_name = self.model.__name__

        condition = [f"{key} = ?" for key in kwargs]
        values = tuple(kwargs.values())
        query = (
            f"DELETE FROM {table_name} WHERE {" AND ".join(condition)}"
            if kwargs
            else f"DELETE FROM {table_name}"
        )
        res = self.model._db.execute(query, values)
        return

    def filter(self, **kwargs):
        if not kwargs:
            raise Exception("Filter cannot be used without key word arguments")

        new_qs = Query(self.model)

        new_qs.filters = self.filters.copy()
        new_qs.filters.append(kwargs)
        return new_qs

    def values(self, *args):
        if not args:
            raise Exception("Cannot csql_result values without arguments!")

        new_qs = Query(self.model)
        new_qs.selected_fields = self.selected_fields.copy()
        new_qs.filters = self.filters.copy()
        table_name = self.model.get_table_name()
        is_missing, missing = self.check_selected_fields(
            table_name, args, self.model._db
        )

        if is_missing:
            raise Exception(
                f" {', '.join(missing)} this fields does not exits in the table"
            )
        new_qs.selected_fields = list(args)

        return new_qs

    def _build_query(self):
        table_name = self.model.get_table_name()

        if self.selected_fields is None:
            query = f"SELECT * FROM {table_name}"
        else:
            query = f"SELECT {', '.join(self.selected_fields)} FROM {table_name}"

        if self.filters:
            conditions = " AND ".join(
                [f"{list(f.keys())[0]} = ?" for f in self.filters]
            )
            values = tuple(list(f.values())[0] for f in self.filters)
            query += f" WHERE {conditions}"
            return query, values
        return None, None

    def sql_result(self):
        query, values = self._build_query()

        if query is None or values is None:
            raise Exception("Something went wrong")

        res = self.model._db.execute(query, values)
        return res.fetchall()

    def iter(self):
        return iter(self.sql_result())

    def repr(self) -> str:
        return repr(self.sql_result())

    def len(self):
        return len(self.sql_result())

    @staticmethod
    def check_selected_fields(table_name: str, columns: Tuple[str], db):
        query = f"SELECT name FROM PRAGMA_TABLE_INFO('{table_name}');"
        res = db.execute(query)
        cols = res.fetchall()
        print(cols)
        missing = [c for c in columns if c not in cols]
        is_missing = all(c in cols for c in cols)
        return is_missing, missing


class Manager:
    def __init__(self, model) -> None:
        self.model = model

    def filter(self, **kwargs):
        return Query(self.model).filter(**kwargs)

    def delete(self, **kwargs):
        return Query(self.model).delete(**kwargs)

    def get(self, **kwargs):
        return Query(self.model).get(**kwargs)

    def all(self):
        return Query(self.model).all()

    def __iter__(self):
        return iter(self.all())

    def __repr__(self):
        return repr(self.all())

    def __len__(self):
        return len(self.all())


class Table:
    _db = None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.objects = Manager(cls)

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

        table_name: str = self.get_table_name()
        columns: list = list(self._get_fields().keys())

        # print("table name: ", table_name)
        # print("column list: ", columns)

        column_names = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        values = tuple(getattr(self, col) for col in columns)

        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

        self._db.execute(query, values)

        return


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
