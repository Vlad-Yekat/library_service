""" модуль сериализации """
from rest_framework import serializers
import datetime
from .errors import JsonErr
from .constants import get_state_by_name


def birth_date_validator(birth_date):
    """ валидация  даты рождения"""
    d = datetime.datetime.now()
    if birth_date > d:
        raise serializers.ValidationError(JsonErr.INVALID_REQUEST["data"])
    else:
        return birth_date


def state_validator(state_name):
    """ валидация книги """
    try:
        get_state_by_name(state_name)
    except KeyError:
        raise serializers.ValidationError(JsonErr.INVALID_REQUEST_STATUS_PARAM["data"])
    else:
        return state_name


class WriterSerializerAdd(serializers.Serializer):
    """   валидатор функции добавления писателя"""

    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=255)
    birth_date = serializers.DateField(validators=[birth_date_validator])


class WriterSerializerEdit(serializers.Serializer):
    """ валидатор функции редактирования писателя"""

    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=255)
    birth_date = serializers.DateField(validators=[birth_date_validator])


class BookSerializerAdd(serializers.Serializer):
    """ валидатор функции добавления книги """

    date_published = serializers.DateField(validators=[birth_date_validator])
    title = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255, validators=[state_validator])


class BookSerializerEdit(serializers.Serializer):
    """ валидатор функции редактировния книги """

    status = serializers.CharField(max_length=255, validators=[state_validator])
