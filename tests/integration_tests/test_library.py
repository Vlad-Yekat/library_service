"""
Интеграционные тесты модели Writer
на вход подаем с клиента http запрос и
смотрим http ответ а также что поменялось в БД
"""
import json
from http import HTTPStatus
import re
import pytest
from django.test import TestCase
from main_room.models import Writer, Books
from main_room.errors import JsonErr
from tests.conftest import FixtureDict

mark = pytest.mark.django_db


class TestAddWriterIntegrity(TestCase):
    """
    SUCCESS TEST(INTEGRATION) - Проверяем функцию добавления сети
    """

    @classmethod
    def setUpClass(cls):
        """ метод установки первоначальных параметров"""
        super(TestAddWriterIntegrity, cls).setUpClass()

    def test_success(self):
        """все параметры корректные"""
        test_add_writer = {
            "method": "add_writer",
            "params": FixtureDict.param_add_writer,
            "jsonrpc": "2.0",
            "id": 123,
        }

        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_add_writer),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Writer.objects.count(), 1)


@pytest.mark.django_db
class TestAddWriterIntegrityError(TestCase):
    """
    EXCEPTION TEST(INTEGRATION) - Проверяем функцию добавления
    """

    @classmethod
    def setUpClass(cls):
        super(TestAddWriterIntegrityError, cls).setUpClass()

    def test_name(self):

        count_obj_before = Writer.objects.count()

        test_add_writer = {
            "method": "add_writer",
            "params": FixtureDict.param_add_writer_without_name,
            "jsonrpc": "2.0",
            "id": 123,
        }

        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_add_writer),
            content_type="application/json",
        )

        count_obj_after = Writer.objects.count()
        response_error = str(response.json()["error"])
        search_string = "name"

        self.assertRegex(response_error, "[^a-z]" + search_string + "[^a-z]")
        self.assertLessEqual(count_obj_after, count_obj_before)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_city(self):
        count_obj_before = Writer.objects.count()

        test_add_writer = {
            "method": "add_writer",
            "params": FixtureDict.param_add_writer_without_city,
            "jsonrpc": "2.0",
            "id": 123,
        }

        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_add_writer),
            content_type="application/json",
        )

        count_obj_after = Writer.objects.count()
        response_error = str(response.json()["error"])
        search_string = "city"

        self.assertRegex(response_error, "[^a-z]" + search_string + "[^a-z]")
        self.assertLessEqual(count_obj_after, count_obj_before)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


@pytest.mark.django_db
class TestEditWriterIntegrity(TestCase):
    """
    SUCCESS TEST (INTEGRATION) функции редактирования

    """

    @classmethod
    def setUpClass(cls):
        super(TestEditWriterIntegrity, cls).setUpClass()

    def test_success(self):
        """все параметры корректны"""
        test_add_writer = {
            "method": "add_writer",
            "params": FixtureDict.param_add_writer,
            "jsonrpc": "2.0",
            "id": 123,
        }

        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_add_writer),
            content_type="application/json",
        )
        response_json = response.json()
        response_answer = response_json["result"]

        edit_param = {"writer_id": response_answer, "city": "Osaka"}
        test_edit_writer = {
            "method": "edit_writer",
            "params": edit_param,
            "jsonrpc": "2.0",
            "id": 123,
        }

        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_edit_writer),
            content_type="application/json",
        )

        print("response", response.json())
        edit_writer = Writer.objects.get(pk=response_answer)

        response_answer_edit = response.json()["result"]

        self.assertEqual(edit_writer.city, "Osaka")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response_answer, response_answer_edit)


@pytest.mark.django_db
class TestEditWriterIntegrityError(TestCase):
    """
    EXCEPTION TEST (INTEGRATION) - Проверяем функцию edit
    с неправильными параметрами
    """

    @classmethod
    def setUpClass(cls):
        super(TestEditWriterIntegrityError, cls).setUpClass()

    def test_bad_method(self):
        """передаем неправильный параметр n1m"""
        test_add_writer = {
            "method": "add_writer",
            "params": FixtureDict.param_add_writer,
            "jsonrpc": "2.0",
            "id": 123,
        }

        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_add_writer),
            content_type="application/json",
        )
        response_json = response.json()
        response_answer = response_json["result"]
        test_edit_writer = {
            "method": "edit_writer",
            "params": {"writer_id": response_answer, "n1m": 123},
            "jsonrpc": "2.0",
            "id": 123,
        }

        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_edit_writer),
            content_type="application/json",
        )
        new_writer = Writer.objects.get(name="Adam")
        response_error = response.json()["error"]
        search_string = "n1m"

        self.assertRegex(response_error["data"], "[^a-z]" + search_string + "[^a-z]")
        self.assertNotEqual(new_writer.name, "Sara")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
