#!/bin/bash

source venv/bin/activate

rm -rf migrations/
flask db init

REVISION_ID="e71b0917e618"

flask db revision --rev-id "$REVISION_ID"

flask db migrate

flask db upgrade