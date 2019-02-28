""" Интеграционные тесты """
from http import HTTPStatus
import json
from unittest import mock
from django.test import TestCase
from tests.conftest import FixtureDict
from main_room.controllers import OTHER_LIB_URL
from main_room.models import Writer


def mocked_requests_get_search_writer(*args, **kwargs):
    """ Этот метод используется для mock ответа вместо модуля requests.get """

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    todos = {"jsonrpc": "2.0", "result": "123456789", "id": 3}
    if args[0] == OTHER_LIB_URL:
        return MockResponse(todos, 200)

    return MockResponse(None, 404)


class TestSearchWriter(TestCase):
    """ SUCCESS TEST(INTEGRATION)
     проверяем функцию search_writer
     """

    @mock.patch("requests.post", side_effect=mocked_requests_get_search_writer)
    def test_fetch(self, mock_get):
        """все параметры корректны"""
        count_before = Writer.objects.count()
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
        count_after = Writer.objects.count()

        test_search_writer = {
            "method": "search_writer",
            "params": FixtureDict.param_add_writer,
            "jsonrpc": "2.0",
            "id": 123,
        }
        response = self.client.generic(
            "POST",
            "",
            data=json.dumps(test_search_writer),
            content_type="application/json",
        )
        response_json = response.json()
        response_answer_search = response_json["result"]

        self.assertEqual(response_answer, response_answer_search)
        self.assertLessEqual(count_before, count_after)
        self.assertEqual(response.status_code, HTTPStatus.OK)

