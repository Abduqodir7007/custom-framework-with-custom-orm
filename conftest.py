from pytest import fixture
from pyframe.app import PyFramework


@fixture
def app():
    return PyFramework()


@fixture
def test_client(app):
    return app.test_session()
