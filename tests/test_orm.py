import pytest
from tests.conftest import db
from pyframe.orm import Database, Table, Column


class TestOrm:

    def test_clear_db(self, db):
        res = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = res.fetchall()
        for table in tables:
            for name in table:
                db.execute(f"DELETE FROM {name}")

        assert 1 == 1

    def test_table_create(self, db: Database):
        class Users(Table):
            name = Column(str)

        db.create(Users)
        res = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = res.fetchall()

        assert ("users",) in tables

    def test_table_info(self, db):
        class Users(Table):
            name = Column(str)

        db.create(Users)
        res = db.execute("PRAGMA table_info(Users)")
        tables = res.fetchall()

        assert tables[0][1] == "name"
        assert tables[0][2] == "TEXT"

    def test_drop_table(self, db: Database):
        class Users(Table):
            name = Column(str)

        db.create(Users)
        db.drop(Users)
        res = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = res.fetchall()

        assert ("users",) not in tables

    def test_data_creation_for_table(self, db):
        class Users(Table):
            name = Column(str)
            password = Column(str)

        db.create(Users)

        user = Users(name="tom", password="easypassword")
        user.save()

        res = db.execute("SELECT * FROM users")
        data = res.fetchall()

        assert data[0][0] == "tom"
        assert data[0][1] == "easypassword"

    def test_all_method(self, db):
        class Users(Table):
            name = Column(str)
            password = Column(str)

        db.create(Users)

        user = Users(name="john", password="easypassword")
        user.save()

        res = user.all()
        assert len(res) == 2

    def test_get_method(self, db):

        class Books(Table):
            name = Column(str)
            author = Column(str)

        db.create(Books)
        book = Books(name="test", author="author")
        book.save()
        res = Books.get(author="author")

        assert res[0] == "test"

    def test_get_method_with_multiple_objects(self, db):

        class User(Table):
            name = Column(str)
            age = Column(int)

        db.create(User)

        user1 = User(name="test_name_1", age=10)
        user2 = User(name="test_name_2", age=10)

        with pytest.raises(Exception):
            res = User.get(age=10)

    def test_delete_method(self, db):
        class Books(Table):
            name = Column(str)
            author = Column(str)

        db.create(Books)
        book = Books(name="book", author="author")
        book.save()

        book.delete(name="book")

        book.save()
        res = db.execute("SELECT * FROM books")

        data = res.fetchall()

        assert book.name not in data

    def test_limit_feature(self, db):
        pass
