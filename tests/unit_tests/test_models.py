""" UNIT тесты модели """
import re
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer
from main_room.models import Books
from main_room.models import Writer

mark = pytest.mark.django_db


class TestWriter(TestCase):
    """
    SUCCESS TEST(UNIT)
    тест создания объекта писателя
    """

    def create_writer(self, **kwargs):
        """ создаем экземпляр модели """
        return Writer.objects.create(
            name=kwargs["name"],
            surname=kwargs["surname"],
            city=kwargs["city"],
            bitrh_date=kwargs["birth_date"],
        )

    def test_writer_creation_success(self):
        """ все параметры корректны """
        result = self.create_writer(
            name="Adam",
            surname="Smiths",
            city="Moscow",
            birth_date="01/01/1982",
        )
        self.assertTrue(isinstance(result, Writer))
        self.assertEqual("Adam", result.name)


class TestWriterError(TestCase):
    """
        EXCEPTION TEST (UNIT)
        создаем запись
        с ошибочными данными
        """

    def test_error_name(self):
        """создаем запись в модели с ошибочным параметром"""
        result = Writer(
            name=123,
            surname="Smiths",
            city="Moscow",
            birth_date="01/01/1982",
        )
        with self.assertRaises(ValidationError) as error:
            result.full_clean()
        self.assertIn("name", str(error.exception))

    def test_error_city(self):
        """создаем запись в модели с ошибочным параметром"""
        result = Writer(
            name="John",
            surname="Smiths",
            city=123,
            birth_date="01/01/1982",
        )
        with self.assertRaises(ValidationError) as error:
            result.full_clean()
        self.assertIn("city", str(error.exception))


@pytest.mark.django_db
class TestBooks(TestCase):
    """
    SUCCESS TEST(UNIT)
    добавляем запись в таблицу модели
    """

    @classmethod
    def setUpClass(cls):
        super(TestBooks, cls).setUpClass()
        mixer.blend("main_room.Books")  # миксер добавления одной записи

    def test_success_add(self):
        """ успешное добавление одной записи"""
        count_obj = Books.objects.count()
        assert count_obj > 0

    def test_success_edit_state(self):
        """ успешное редактирование """
        tested_book = Books.objects.create()
        tested_book.edit_book(status="DRAFT")
        self.assertEqual(tested_book.status, 1)


class TestBooksError(TestCase):
    """
    EXCEPTION TEST(UNIT)
    добавляем запись в таблицу модели
    с шибочными параметрами
    """

    def test_error_edit_date_published(self):
        """добавляем диапазон с неуказанием параметра"""
        tested_writer = Writer.objects.create()
        tested_writer.save()
        dict_param = {"date_published": 123}
        tested_object = Books()
        with self.assertRaises(KeyError) as error:
            tested_object.add_book(
                date_published=dict_param["date_published"],
            )
        self.assertIn("date_published", str(error.exception))


