import os
import django
from django.conf import settings
import copy
import pytest


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings")


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "library_db"),
        "USER": "root",
        "PASSWORD": "12345",
        "HOST": "127.0.0.1",  # Or an IP Address that your DB is hosted on
        "PORT": "3305",
    }


def pytest_configure():
    settings.DEBUG = True
    django.setup()


class FixtureDict:
    param_add_writer = {
        "name": "James",
        "surname": "Bond",
        "city": "London",
        "birth_date": "23/01/1977",
    }

    param_add_writer_without_name = {
        "surname": "Bond",
        "city": "London",
        "birth_date": "23/01/1977",
    }

    param_add_writer_without_surname = {
        "name": "James",
        "city": "London",
        "birth_date": "23/01/1977",
    }

    param_add_writer_without_city = {
        "name": "James",
        "surname": "Bond",
        "birth_date": "23/01/1977",
    }

    param_add_writer_without_birth_date = {
        "name": "James",
        "surname": "Bond",
        "city": "London",
    }

    param_add_writer_error_name = copy.copy(param_add_writer)
    param_add_writer_error_name["name"] = 123

    param_add_writer_error_birth_date = copy.copy(param_add_writer)
    param_add_writer_error_birth_date["birth_date"] = 123
