# Kahani

Be A Good Cineme Lover

## Setting up Docker

docker-compose up -d

# Activate virtualenv

source venv/bin/activate

# Migration

flask db init
flask db revision --rev-id ID
flask db migrate
flask db upgrade
