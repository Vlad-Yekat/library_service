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


def get_response(args):
    """ вынесем отдельно запрос на микросервис сторонне библиотеки"""
    return requests.post(OTHER_LIB_URL, json=args).json()


def validate(function):
    """ процедура валидации входных параметров """

    def wrapped(args):
        """ проверяем json схему """
        validate_json_error = json_converter.validate_json(args, function.__name__)
        if validate_json_error:
            return return_invalid_request(validate_json_error)
        return function(args)

    return wrapped


@validate
def add_writer(args):
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
            name=args["name"],
            surname=args["surname"],
            city=args["city"],
            birth_date=args["birth_date"],
        )
        # print(connections['default'].queries)
    except ValidationError as error:
        return return_invalid_request(error)

    return new_writer.id


@validate
def edit_writer(args):
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
    writer_id = args["writer_id"]

    try:
        writer_record = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_WRITER}

    writer_record.edit_writer(city=args["city"])
    return writer_id


@validate
def search_writer(args):
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
    other_lib_params = {"method": "search_writer_moscow", "params": args}
    other_lib_jsonrpc = json_converter.prepare_for_jsonrpc(other_lib_params, 1)
    response_other_lib = get_response(other_lib_jsonrpc)
    if "result" in response_other_lib:
        pass  # deleted for this example

    try:
        writer_record = Writer.objects.get(
            Q(name__exact=args["name"]),
            Q(surname__exact=args["surname"]),
            Q(birth_date__exact=args["birth_date"]),
        )
    except Writer.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_WRITER}

    return writer_record.id


@validate
def del_writer(args):
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
    writer_id = args["writer_id"]

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
def add_book(args):
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
        writer_id=args["writer_id"],
        date_published=args["date_published"],
        title=args["title"],
        state=args["state"],
    )
    return answer_from_model.get("result") or answer_from_model.get("error")


@validate
def edit_book(args):
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
    answer = args["book_id"]
    try:
        edit_book_record = Books.objects.get(pk=args["book_id"])
        edit_book_record.edit_book(state=args["state"])
    except Books.DoesNotExist:
        answer = {"error": JsonErr.DATA_NOT_FOUND_BOOK}

    return answer


@validate
def del_book(args):
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
    answer = args["book_id"]
    try:
        deleted_book = Books.objects.get(pk=answer)
    except Books.DoesNotExist:
        return {"error": JsonErr.DATA_NOT_FOUND_BOOK}
    deleted_book.mark_deleted()

    return answer
