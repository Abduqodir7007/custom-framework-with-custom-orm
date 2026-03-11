from pytest import fixture
from app import PyFramework

@fixture
def app():
    return PyFramework()

@fixture
def test_client(app):
    return app.test_session()
