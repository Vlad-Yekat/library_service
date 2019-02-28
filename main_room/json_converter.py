"""
json - rpc согласно стандарта имеет следующие примеры
    into {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}
    form {"jsonrpc": "2.0", "result": 19, "id": 1}
"""

from jsonschema import validate
from main_room.config_dir import MAIN_CONF


def prepare_for_jsonrpc(arg1, id_answer):
    """ преобразуем словарь в стандарт ответа json rpc"""
    dict_head = {"jsonrpc": "2.0"}
    dict_jsonrpc = {**dict_head, **arg1}

    if id_answer:
        dict_jsonrpc["id"] = id_answer
    else:
        dict_jsonrpc["result"] = "Notify"
    return dict_jsonrpc


def validate_json(param, name_func):
    """ библиотека валидации входных параметров через файл настроек"""
    param_name = "validate_" + name_func + ".json"
    schema = MAIN_CONF[param_name]
    return validate(param, schema)
