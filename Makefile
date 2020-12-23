COMPOSE_FILES := -f docker-compose.yml
MANAGE_HOST := 192.168.1.101
MANAGE_PORT := 8080
BASE := nu_lessons


up:
	docker-compose $(COMPOSE_FILES) up

start:
	docker-compose $(COMPOSE_FILES) start

stop:
	docker-compose $(COMPOSE_FILES) stop

build:
	docker-compose $(COMPOSE_FILES) build

build_clean:
	docker-compose $(COMPOSE_FILES) build --no-cache

build_base:
	docker build --no-cache -f ./compose/Dockerfile.base -t ${BASE} .

app:
	python ./manage.py runserver ${MANAGE_HOST}:${MANAGE_PORT}

shell:
	python ./manage.py shell_plus

collectstatic:
	python ./manage.py collectstatic --noinput

compress:
	python ./manage.py compress -v 0

migrations:
	python ./manage.py makemigrations

migrate:
	python ./manage.py migrate

superuser:
	python ./manage.py createsuperuser

install:
	pip install -r requirements.txt
