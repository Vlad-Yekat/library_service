"""
В данном модуле контроллеры
"""
import os
import requests
from django.db.models import ProtectedError
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from .models import Writer
from .models import Books
from .errors import JsonErr, return_invalid_request
from . import json_converter


OTHER_LIB_URL = (
    os.getenv("MOSCOW_LIBRARY_HOST", "http://localhost")
    + ":"
    + os.getenv("MOSCOW_LIBRARY_PORT", "8080")
)


def get_response(**kwargs):
    """ вынесем отдельно запрос на микросервис сторонне библиотеки"""
    return requests.post(OTHER_LIB_URL, json=kwargs).json()


def validate(function):
    """ процедура валидации входных параметров """

    def wrapped(**kwargs):
        """ проверяем json схему """
        validate_json_error = json_converter.validate_json(kwargs, function.__name__)
        if validate_json_error:
            return return_invalid_request(validate_json_error)
        return function(kwargs)

    return wrapped


@validate
def add_writer(**kwargs):
    """
    :param:
    {
     "jsonrpc": "2.0",
     "method": "add_writer",
     "params": {
                },
     "id": 3
    }
    :return:
    {"jsonrpc": "2.0", "result": 1, "id": 3}
    """
    new_writer = Writer()
    try:
        new_writer.add_writer(
            name=kwargs["name"],
            surname=kwargs["surname"],
            city=kwargs["city"],
            birth_date=kwargs["birth_date"],
        )
        # print(connections['default'].queries)
    except ValidationError as error:
        return return_invalid_request(error)

    return new_writer.id


@validate
def edit_writer(**kwargs):
    """
    :param:
    {
     "jsonrpc": "2.0",
     "method": "edit_writer",
     "params": {
               },
     "id": 3
    }
    :return:
    {"jsonrpc": "2.0", "result": 1, "id": 3}
    """
    writer_id = kwargs["writer_id"]

    try:
        writer_record = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_WRITER}

    writer_record.edit_writer(city=kwargs["city"])
    return writer_id


@validate
def search_writer(**kwargs):
    """
    :param:
    {
     "jsonrpc": "2.0",
     "method": "search_writer",
     "params": {
               },
     "id": 3
    }
    :return:
    {"jsonrpc": "2.0", "result": 1, "id": 3}
    """
    other_lib_params = {"method": "search_writer_moscow", "params": kwargs}
    other_lib_jsonrpc = json_converter.prepare_for_jsonrpc(other_lib_params, 1)
    response_other_lib = get_response(other_lib_jsonrpc)
    if "result" in response_other_lib:
        pass  # deleted for this example

    try:
        writer_record = Writer.objects.get(
            Q(name__exact=kwargs["name"]),
            Q(surname__exact=kwargs["surname"]),
            Q(birth_date__exact=kwargs["birth_date"]),
        )
    except Writer.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_WRITER}

    return writer_record.id


@validate
def del_writer(**kwargs):
    """
    :param:
    {
     "jsonrpc": "2.0",
     "method": "del_writer",
     "params": {
               },
      "id": 3
    }
    :return:
    {"jsonrpc": "2.0", "result": 1, "id": 3}
    """
    writer_id = kwargs["writer_id"]

    try:
        deleted_writer = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_WRITER}

    try:
        deleted_writer.delete()
    except ProtectedError:
        return {"error": JsonErr.PROTECTED_ERROR_FOREIGN_KEY}

    return writer_id


@validate
def add_book(**kwargs):
    """
    :param:
    {
     "method": "add_book",
     "params": {
               },
     "jsonrpc": "2.0",
     "id": 123
    }
    :return:
    {"jsonrpc": "2.0", "result": 1, "id": 123}
    """
    new_book = Books()

    answer_from_model = new_book.add_book(
        writer_id=kwargs["writer_id"],
        date_published=kwargs["date_published"],
        title=kwargs["title"],
        state=kwargs["state"],
    )
    return answer_from_model.get("result") or answer_from_model.get("error")


@validate
def edit_book(**kwargs):
    """
    :param:
    {
        "method": "edit_book",
        "params": {
        },
        "jsonrpc": "2.0",
        "id": 123,
    }
    :return:
    {"jsonrpc": "2.0", "result": 2, "id": 123}
    """
    answer = kwargs["book_id"]
    try:
        edit_book_record = Books.objects.get(pk=kwargs["book_id"])
        edit_book_record.edit_book(state=kwargs["state"])
    except Books.DoesNotExist:
        answer = {"error": JsonErr.DATA_NOT_FOUND_BOOK}

    return answer


@validate
def del_book(**kwargs):
    """
    :param:
    {
     "jsonrpc": "2.0",
     "method": "del_book",
     "params": {
               },
      "id": 3
    }
    :return:
    {"jsonrpc": "2.0", "result": 1, "id": 3}
    """
    answer = kwargs["book_id"]
    try:
        deleted_book = Books.objects.get(pk=answer)
    except Books.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_BOOK}
    deleted_book.mark_deleted()

    return answer
