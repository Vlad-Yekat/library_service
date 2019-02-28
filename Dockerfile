FROM python:3.7-alpine

EXPOSE 5000
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .

RUN apk add --no-cache gcc python3-dev libffi-dev musl-dev linux-headers mariadb-dev mariadb-client

RUN pip3 install -r requirements.txt

ADD . /app/

CMD ["./entrypool.sh"]


# CMD python3 manage.py runserver 0.0.0.0:8000
# CMD gunicorn ip_service.wsgi -b 0.0.0.0:5000

