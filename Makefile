# Этот Makefile предназначен разработчика.

# Остановить контейнер's
stop-local:
	-docker container stop libraryservice_web_1
	-docker container stop libraryservice_db_1

remove-local:
	@make stop-local
	-docker container rm libraryservice_web_1
	-docker container rm libraryservice_db_1

remove-image-local:
	@make stop-local
	-docker image rm libraryservice_web
	-docker image rm libraryservice_db

# для целей проверки работоспособности локально.
build-run-compose-local:
	docker-compose up -d

test-local:
	docker container exec -it libraryservice_web_1 pytest .

log-local:
	docker container logs libraryservice_web_1

# подключение к запущенному контейнеру mysql:
exec-local-sql:
	docker container exec -it libraryservice_db_1 bash

down-compose-local:
	docker-compose down

