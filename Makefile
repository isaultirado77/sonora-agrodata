.PHONY: etl\
		extract\
		transform\
		load\
		inspect\
		clean\
		build\
		up\
		down\
		run-jupyter\
		docker-logs\
		docker-clean\

		

# Local

etl: extract transform load

extract:
	uv run python -m etl.extract

transform:
	uv run python -m etl.transform

load:
	uv run python -m etl.load

run_jupyter:
	uv run jupyter lab --ip=0.0.0.0 --port=8888 --allow-root

inspect:
	uv run python scripts/inspect_db.py

clean:
	rm -rf data/processed/*
	rm -rf data/interim/*
	rm -rf data/raw/*

# Continer 

# Build images
build:
	docker compose build

# Levantar servicios (etl + jupyter)
up:
	docker compose up

# Detener servicios
down:
	docker compose down

# Ver logs de Docker compose
docker-logs:
	docker compose logs -f

# Clean docker
docker-clean:
	docker system prune -a --volumes -f
