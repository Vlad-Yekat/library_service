"""  Модели писателя и книг """
from django.db import models
from .errors import JsonErr
from .serializers import WriterSerializerAdd, WriterSerializerEdit
from .serializers import BookSerializerAdd, BookSerializerEdit
from .constants import get_state_by_name, STATE_RANGE


class Binary365Field(models.Field):
    """
    кастомный класс для того чтобы в MYSQL был тип VarBinary(365)
    а не LONGBLOB как при стандартном типе django - BinaryField
    """
    class TestHook:
        """
        Для корретной работы Pytest с нашим binary field
        """

        class VirtualDict:
            """ для корректной работы pytest """
            name = "VARBINARY()"
            null = True
            blank = True

            def has_default(self):
                return False

            def save(self):
                return True

        some_row = VirtualDict()
        fields = {some_row}
        name = "VARBINARY()"
        local_many_to_many = {}

    _meta = TestHook()

    def __repr__(self):
        return "4"

    def __str__(self):
        return "4"

    def save(self):
        return

    def db_type(self, connection):
        return "VARBINARY(365)"


class Writer(models.Model):
    """ модель где хранятся писатели книг"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    city = models.CharField(max_length=45)
    birth_date = models.DateField()

    def add_writer(self, name, surname, city, birth_date):
        """добавляем автора + заодно какие то вычисления и проверки"""
        data = {
            "name": name,
            "surname": surname,
            "city": city,
            "birth_date": birth_date,
        }
        result_serializer = WriterSerializerAdd(data=data)
        if result_serializer.is_valid(raise_exception=True):
            self.name = name
            self.surname = surname
            self.city = city
            self.birth_date = birth_date
            self.save()

    def edit_writer(self, name, surname, city, birth_date):
        """ функция редактирования только города
        """
        data = {"name": name, "surname": surname, "city": city, "birth_date": birth_date}
        result_serializer = WriterSerializerEdit(data=data)
        if result_serializer.is_valid():
            self.city = city
            self.save()


class Books(models.Model):
    """ модель где хранятся книги"""
    id = models.BigAutoField(primary_key=True)
    writer = models.ForeignKey("Writer", on_delete=models.PROTECT)  # ProtectedError
    date_published = models.DateField()
    title = models.CharField(max_length=245)
    last_updated = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=STATE_RANGE, null=True)
    barcode = Binary365Field(null=False, unique=True)

    def add_book(self, writer_id, date_published, title, state):
        """ добавляем книгу + проверки и вычисления """
        data = {
            "writer_id": writer_id, "date_published": date_published, "title": title, "state": state
        }
        result_serializer = BookSerializerAdd(data=data)

        if not result_serializer.is_valid():
            return {"error": result_serializer.errors}

        try:
            writer_new = Writer.objects.get(pk=writer_id)
        except Writer.DoesNotExist:
            return JsonErr.DATA_NOT_FOUND_NET

        self.writer = writer_new
        self.date_published = date_published
        self.title = title
        self.barcode = bin(self.id)
        self.status = get_state_by_name(state)
        self.save()
        return {"result": self.id}

    def edit_book(self, state):
        """единственно что можем редактировать это состояние"""
        data = {"state": state}
        result_serializer = BookSerializerEdit(data=data)
        if result_serializer.is_valid():
            self.status = get_state_by_name(state)
            self.save()

    def mark_deleted(self):
        """ так как мы не удаляем а только списываем"""
        status_num = get_state_by_name("CANCELLED")
        self.status = status_num
        self.save()

