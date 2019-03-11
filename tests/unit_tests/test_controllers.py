""" UNIT тесты """
import re
from django.test import TestCase
import pytest
from jsonschema.exceptions import ValidationError
from main_room.controllers import add_writer, edit_writer, del_writer
from main_room.controllers import add_book, edit_book, del_book
from tests.conftest import FixtureDict

mark = pytest.mark.django_db


@pytest.mark.django_db
class TestAddWriter(TestCase):
    """
    SUCCESS TEST(UNIT)
    Проверяем функцию добавления автора """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestAddWriter, cls).setUpClass()

    def test_success(self):
        """ все параметры корректны """
        param = FixtureDict.param_add_writer
        answer = add_writer(param)

        self.assertIsInstance(answer, int)


@pytest.mark.django_db
class TestAddWriterError(TestCase):
    """
    EXCEPTION TEST(UNIT)
    Проверяем функцию добавления с ошибочными данными
    """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestAddWriterError, cls).setUpClass()

    def test_name(self):
        param = FixtureDict.param_add_writer_error_name
        search_string = "name"
        with self.assertRaises(ValidationError) as error:
            add_writer(param)

        self.assertRegex(str(error.exception), "[^a-z]" + search_string + "[^a-z]")

    def test_birth_date(self):
        param = FixtureDict.param_add_writer_error_birth_date
        search_string = "birth_date"
        with self.assertRaises(ValidationError) as error:
            add_writer(param)

        self.assertRegex(str(error.exception), "[^a-z]" + search_string + "[^a-z]")

    def test_city(self):
        param = FixtureDict.param_add_writer_without_city
        search_string = "city"
        with self.assertRaises(ValidationError) as error:
            add_writer(param)

        self.assertRegex(str(error.exception), "[^a-z]" + search_string + "[^a-z]")

    def test_surname(self):
        param = FixtureDict.param_add_writer_without_surname
        search_string = "surname"
        with self.assertRaises(ValidationError) as error:
            add_writer(param)

        self.assertRegex(str(error.exception), "[^a-z]" + search_string + "[^a-z]")


@pytest.mark.django_db
class TestEditWriter(TestCase):
    """ SUCCESS TEST(UNIT)
    Проверяем функцию изменения параметров автора """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestEditWriter, cls).setUpClass()

    def test_success(self):
        """ все параметры корректны """
        param = FixtureDict.param_add_writer
        answer = add_writer(param)

        param = {"writer_id": answer, "city": "Osaka"}
        answer = edit_writer(param)

        self.assertIsInstance(answer, int)


@pytest.mark.django_db
class TestEditWriterError(TestCase):
    """
    EXCEPTION TEST(UNIT)
    Проверяем функцию изменения параметров

    """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestEditWriterError, cls).setUpClass()

    def test_city(self):
        """ передан неправильный, числовой параметр """
        param = FixtureDict.param_add_writer_without_city
        search_string = "city"
        with self.assertRaises(ValidationError) as error:
            edit_writer(param)

        self.assertRegex(str(error.exception), "[^a-z]" + search_string + "[^a-z]")


@pytest.mark.django_db
class TestDelWriter(TestCase):
    """ SUCCESS TEST(UNIT)
    проверяем функцию удаления
    """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestDelWriter, cls).setUpClass()

    def test_success(self):
        """ все параметры переданы корректно """
        param = FixtureDict.param_add_writer
        answer = add_writer(param)
        result = answer

        param = {"writer_id": result}
        answer = del_writer(param)

        self.assertIsInstance(answer, int)


@pytest.mark.django_db
class TestDelWriterError(TestCase):
    """ EXCEPTION TEST(UNIT)
    Проверяем функцию удаления автора с ошибочным параметром
    """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestDelWriterError, cls).setUpClass()

    def test_id_error(self):
        """ передан неправильный параметр id """
        param = {"wrt_id": "1111"}
        search_string = "wrt_id"
        with self.assertRaises(ValidationError) as error:
            del_writer(param)
        self.assertRegex(str(error.exception), "[^a-z]" + search_string + "[^a-z]")


@pytest.mark.django_db
class TestAddBook(TestCase):
    """
    SUCCESS TEST(UNIT)
    тестирование добавления пула сетей
    """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestAddBook, cls).setUpClass()

    def test_success(self):
        """ все параметры корректны """
        param = FixtureDict.param_add_writer
        answer = add_writer(param)
        result_writer = answer

        param = {
            "writer_id": result_writer,
            "title": "Capital",
            "state": "DRAFT",
            "date_published": "2019-01-01",
        }
        answer = add_book(param)

        self.assertIsInstance(answer, int)


@pytest.mark.django_db
class TestAddBookError(TestCase):
    """
    EXCEPTION TEST(UNIT)
    тестирование добавления пула сетей с ошибочными данными
    """

    @classmethod
    def setUpClass(cls):
        """ Обязательный метод установки начальных параметров"""
        super(TestAddBookError, cls).setUpClass()

    def test_id_error(self):
        """неправильный параметр writ_id"""
        param = {"wrt_id": "1111"}
        search_string = "wrt_id"
        with self.assertRaises(ValidationError) as error:
            add_book(param)
        self.assertRegex(str(error.exception), "[^a-z]" + search_string + "[^a-z]")
