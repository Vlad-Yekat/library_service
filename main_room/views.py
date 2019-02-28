""" модуль представления для джанги """
import json
import copy
from django.http import JsonResponse
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt
from jsonschema.exceptions import ValidationError
from . import json_converter
from . import controllers
from .errors import JsonErr


def add_to_answer_list(name_func, params_func, id_answer):
    """ данная функция запускает контроллеры
     и возвращает ответ в формате json для добавления в batch"""
    try:
        func = getattr(controllers, name_func)
        answer = func(params_func)
        if isinstance(answer, (int, str)):
            answer = {"result": answer}
        else:
            id_answer = "null"
    except AttributeError as error:
        message_error = copy.copy(JsonErr.METHOD_NOT_FOUND_OTHER)
        message_error["data"] = str(error)
        return {"jsonrpc": "2.0", "error": message_error}
    except ValidationError as error:
        message_error = copy.copy(JsonErr.INVALID_REQUEST_JSON_PARAM)
        message_error["data"] = str(error)
        return {"jsonrpc": "2.0", "error": message_error}
    answer = json_converter.prepare_for_jsonrpc(answer, id_answer)
    return answer


@csrf_exempt
def index(request):
    """ основная вьюшка куда все приходит """
    answer_list = []
    status = HTTPStatus.OK  # у batch всегда ок (jsonrpcserver также)
    try:
        if not request.body:
            status = HTTPStatus.NO_CONTENT
            message_error = copy.copy(JsonErr.PARSE_ERROR_OTHER)
            answer_list.append({"jsonrpc": "2.0", "error": message_error, "id": None})
        else:
            input_json = json.loads(request.body)
            is_batch = isinstance(input_json, list)
            data = input_json if is_batch else [input_json]

            for inp in data:
                name_func = inp["method"]
                params_func = inp["params"] or {}
                id_answer = inp["id"]
                answer_list.append(
                    add_to_answer_list(name_func, params_func, id_answer)
                )

    except ValueError as error:
        message_error = copy.copy(JsonErr.PARSE_ERROR_OTHER)
        message_error["data"] = str(error)
        answer_list.append({"jsonrpc": "2.0", "error": message_error, "id": None})

    if len(answer_list) == 1:
        answer_list = answer_list[0]
        if "error" in answer_list:
            status = HTTPStatus.BAD_REQUEST

    return JsonResponse(status=status, data=answer_list, safe=False)
