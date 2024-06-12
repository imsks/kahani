# Build App
build:
	docker-compose build

# Run App
run:
	docker-compose up -d

# Down App
down:
	docker-compose down

# Create virtualenv
create:
	pip install -r requirements.txt
	python3 -m venv venv

# Migrate database
migrate:
	flask db init
	flask db migrate
	flask db upgrade