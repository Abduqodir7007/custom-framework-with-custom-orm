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

        res = user.objects.all()
        assert len(res) == 2

    def test_get_method(self, db):

        class Books(Table):
            name = Column(str)
            author = Column(str)

        db.create(Books)
        book = Books(name="test", author="author")
        book.save()
        res = Books.objects.get(author="author")

        assert res[0] == "test"

    def test_get_method_with_multiple_objects(self, db):

        class User(Table):
            name = Column(str)
            age = Column(int)

        db.create(User)

        user1 = User(name="test_name_1", age=10)
        user2 = User(name="test_name_2", age=10)

        with pytest.raises(Exception):
            res = User.objects.get(age=10)

    def test_delete_method(self, db):
        class Books(Table):
            name = Column(str)
            author = Column(str)

        db.create(Books)
        book = Books(name="book", author="author")
        book.save()

        Books.objects.delete(name="book")

        res = db.execute("SELECT * FROM books")
        data = res.fetchall()

        assert book.name not in data

    def test_limit_feature(self, db):
        pass

    def test_values_method(self, db):

        class Person(Table):
            name = Column(str)
            age = Column(int)
            # email = Column(str)
        db.create(Person)

        p1 = Person(name="Tom", age=6, email="")
        p1.save()

        person = Person.objects.filter(name="Tom").values("name")
        result = list(person)
        assert "Tom" in result[0]

    def test_manager_iter_len_repr(self, db):
        class User(Table):
            name = Column(str)
            age = Column(int)

        db.create(User)
        User(name="alice", age=30).save()
        User(name="bob", age=25).save()

        # Test __iter__
        names = [user[0] for user in User.objects]
        assert "alice" in names and "bob" in names
        print(User.objects)
        # Test __len__
        assert len(User.objects) == 2

        # Test __repr__ (should contain both names)
        rep = repr(User.objects)
        assert "alice" in rep and "bob" in rep

        # Test print (should not error, output not asserted)
        print(User.objects)
