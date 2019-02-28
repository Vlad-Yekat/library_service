"""
В данном модуле контроллеры
"""

from django.db.models import ProtectedError
from rest_framework.exceptions import ValidationError
from .models import Writer
from .models import Books
from .errors import JsonErr, return_invalid_request
from . import json_converter


def validate(function):
    """ процедура валидации входных параметров """

    def wrapped(params):
        """ проверяем json схему """
        validate_json_error = json_converter.validate_json(params, function.__name__)
        if validate_json_error:
            return return_invalid_request(validate_json_error)
        return function(params)

    return wrapped


@validate
def add_writer(params):
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
            name=params["name"],
            surname=params["surname"],
            city=params["city"],
            birth_date=params["birth_date"],
        )
    except ValidationError as error:
        return return_invalid_request(error)

    return new_writer.id


@validate
def edit_writer(params):
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
    writer_id = params["writer_id"]

    try:
        writer_record = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_WRITER}

    writer_record.edit_writer(
        name=params["name"],
        surname=params["surname"],
        city=params["city"],
        birth_date=params["birth_date"],
    )
    return writer_id


@validate
def del_writer(params):
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
    writer_id = answer = params["writer_id"]

    try:
        deleted_writer = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_WRITER}

    try:
        deleted_writer.delete()
    except ProtectedError:
        return {"error": JsonErr.PROTECTED_ERROR_FOREIGN_KEY}

    return answer


@validate
def add_book(params):
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
        writer_id=params["writer_id"],
        date_published=params["date_published"],
        title=params["title"],
        state=params["state"],
    )
    return answer_from_model.get("result") or answer_from_model.get("error")


@validate
def edit_book(params):
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
    answer = params["book_id"]
    try:
        edit_book_record = Books.objects.get(pk=params["book_id"])
        edit_book_record.edit_book(state=params["state"])
    except Books.DoesNotExist:
        answer = {"error": JsonErr.DATA_NOT_FOUND_BOOK}

    return answer


@validate
def del_book(params):
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
    answer = params["book_id"]
    try:
        deleted_book = Books.objects.get(pk=answer)
    except Books.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_BOOK}
    deleted_book.mark_deleted()

    return answer
