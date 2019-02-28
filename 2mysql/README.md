#1 inside

docker exec -it mysql bash

mysql -uroot -p

show databases;

create database library_db;

#2 From Django

python3 manage.py migrate

#3 inside after migrate in  mysql
use library_db;

show tables;

select * from mainroom_writer;