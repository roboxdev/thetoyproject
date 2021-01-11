build: build-docker up
	# builds and starts the docker container

build-docker:
	docker-compose build

up:
	# starts the docker container
	docker-compose up -d

ssh:
	# SSH into the blogapp container
	docker-compose exec web bash

server:
	# executes the django python manage.py runserver command inside the running blogapp container
	docker-compose exec web python manage.py runserver 0.0.0.0:8019

down:
	# stops the docker container
	docker-compose down

flake8:
	# runs flake8 linting on the app
	docker-compose run --rm --entrypoint flake8 web --format='%(path)s:%(row)d,%(col)d:%(code)s:%(text)s:https://lintlyci.github.io/Flake8Rules/rules/%(code)s.html'

test:
	# runs your python tests
	docker-compose run --rm web test

logs:
	docker-compose logs -f

migrate:
	docker-compose run --rm web migrate

status:
	docker-compose ps -a
