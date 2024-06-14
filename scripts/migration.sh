#!/bin/bash

source venv/bin/activate

rm -rf migrations/
flask db init

REVISION_ID="ee1a0f9cc38b"

flask db revision --rev-id "$REVISION_ID"

flask db migrate

flask db upgrade