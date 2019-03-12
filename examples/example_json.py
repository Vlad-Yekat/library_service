""" В этом модуле примеры внешних запросов """
import requests
import json


def main():
    """ можно запускать из IDE или консоли"""
    url_library_service = "http://localhost:8000"
    # headers = {"content-type": "application/json"}

    test_add_writer = {
        "method": "add_writer",
        "params": {
            "name": "Adam",
            "surname": "Smith",
            "city": "Kirkcaldy",
            "birth_date": "1723-06-17",
        },
        "jsonrpc": "2.0",
        "id": 123,
    }

    response = requests.post(url_library_service, json=test_add_writer).json()
    print("->", json.dumps(test_add_writer, indent=4, sort_keys=False))
    print("<-", response)

    assert response["jsonrpc"]
    assert response["id"] == 123
    writer_id = response["result"]

    test_add_book = {
        "method": "add_book",
        "params": {
            "writer_id": writer_id,
            "date_published": "1759-01-01",
            "title": "The Theory of Moral Sentiments",
            "state": "PUBLISHED",
        },
        "jsonrpc": "2.0",
        "id": 123,
    }

    response = requests.post(url_library_service, json=test_add_book).json()
    print("->", json.dumps(test_add_book, indent=4, sort_keys=False))
    print("<-", response)

    assert response["jsonrpc"]
    assert response["id"] == 123


if __name__ == "__main__":
    main()
