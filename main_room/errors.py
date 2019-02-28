""" в этом модуле собраны все коды ошибок"""
import copy


def return_invalid_request(error):
    """ для исключения DRY """
    error_dict = copy.copy(JsonErr.INVALID_REQUEST_OTHER_PARAM)
    error_dict["data"] = str(error)
    return {"error": error_dict}


class JsonErr:
    """
    All code from jsonrpc documentation, wiki, stackoverflow
    """

    INVALID_REQUEST = -32600
    PARSE_ERROR = -32700
    METHOD_NOT_FOUND = -32601
    DATA_NOT_FOUND = -32602
    PROTECTED_ERROR = -32655

    INVALID_REQUEST_STATUS_PARAM = {
        "code": INVALID_REQUEST,
        "message": "Invalid Request",
        "data": "Non valid 'status' param",
    }

    INVALID_REQUEST_OTHER_PARAM = {
        "code": INVALID_REQUEST,
        "message": "Invalid Request",
        "data": "Invalid Request. Unknown parameter ",
    }

    INVALID_REQUEST_JSON_PARAM = {
        "code": INVALID_REQUEST,
        "message": "Invalid Request",
        "data": "Error in JSON SCHEMA validation. ",
    }

    DATA_NOT_FOUND_WRITER = {
        "code": DATA_NOT_FOUND,
        "message": "Data not found",
        "data": "Cannot found writer, object does not exist",
    }

    DATA_NOT_FOUND_BOOK = {
        "code": DATA_NOT_FOUND,
        "message": "Data not found",
        "data": "Cannot found book, object does not exist",
    }

    PROTECTED_ERROR_FOREIGN_KEY = {
        "code": PROTECTED_ERROR,
        "message": "Protected error",
        "data": "Cannot delete - referenced foreign key",
    }

    METHOD_NOT_FOUND_OTHER = {
        "code": METHOD_NOT_FOUND,
        "message": "Method not found",
        "data": "Method not found ",
    }

    PARSE_ERROR_OTHER = {
        "code": PARSE_ERROR,
        "message": "Parse error",
        "data": "Parse error ",
    }
