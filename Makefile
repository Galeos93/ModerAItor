include LABEL_STUDIO.env
export $(shell sed 's/=.*//' LABEL_STUDIO.env)

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

run-annotator:
	label-studio & python moderaitor/label_studio/create_project.py

build-docker:
	docker build -f docker/moderaitor/Dockerfile -t moderaitor .