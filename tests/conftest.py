from pytest import fixture
import sys
import os
from main import PyFramework

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@fixture
def app():
    return PyFramework()


@fixture
def test_client(app):
    return app.test_session()
