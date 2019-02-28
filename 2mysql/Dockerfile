FROM percona
LABEL maintainer="Vlad Rybin <vladislavi@mail.ru>"

COPY mysql_mysqld.cnf /etc/mysql/percona-server.conf.d/mysqld.cnf
COPY test_db/database.sql /docker-entrypoint-initdb.d/
