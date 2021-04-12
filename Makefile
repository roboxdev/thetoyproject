build: build-docker up
	# builds and starts the docker container

build-docker:
	# builds the docker container
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

up:
	# starts the docker container
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

dev:
	# starts containers in development mode
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

ssh:
	# SSH into the blogapp container
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web bash

server:
	# executes the django python manage.py runserver command inside the running blogapp container
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py runserver 0.0.0.0:8019

down:
	# stops the docker container
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

flake8:
	# runs flake8 linting on the app
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --entrypoint flake8 web --format='%(path)s:%(row)d,%(col)d:%(code)s:%(text)s:https://lintlyci.github.io/Flake8Rules/rules/%(code)s.html'

test:
	# runs your python tests
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web test

logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

migrate:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web migrate

status:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml ps -a
