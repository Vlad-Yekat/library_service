""" модуль memoization"""
import os

import json
from django.conf import settings

__all__ = ["MAIN_CONF"]


class Memoization:
    """ класс со словарем конфигураций """

    def __init__(self):
        self.__cache = {}

    def __load(self, name):
        if name in self.__cache:
            return
        path = os.path.join(settings.BASE_DIR, "main_room", "config_dir", name)
        with open(path) as file_json:
            self.__cache[name] = json.load(file_json)

    def __getitem__(self, item):
        self.__load(item)
        return self.__cache[item]


MAIN_CONF = Memoization()
