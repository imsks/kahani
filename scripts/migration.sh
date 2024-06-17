#!/bin/bash

source venv/bin/activate

rm -rf migrations/
flask db init

REVISION_ID="1fdd56d2a705"

flask db revision --rev-id "$REVISION_ID"

flask db migrate

flask db upgrade