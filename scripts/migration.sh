#!/bin/bash

source venv/bin/activate

rm -rf migrations/
flask db init

REVISION_ID="f4ae8a75046b"

flask db revision --rev-id "$REVISION_ID"

flask db migrate

flask db upgrade