env-create:
	tox -e moderaitor

env-compile:
	pip-compile --resolver=backtracking requirements.in

lint:
	pylint moderaitor

test:
	if [ -z "$(MODEL_VERSION)" ]; then pytest tests; else MODEL_VERSION=$(MODEL_VERSION) pytest tests; fi

run-app:
	docker compose -f docker/docker-compose.yml --project-directory . up --build

build-docker:
	docker build -f docker/moderaitor/Dockerfile -t moderaitor .