#!/bin/bash

source venv/bin/activate

rm -rf migrations/
flask db init

REVISION_ID="fc04be48a6be"

flask db revision --rev-id "$REVISION_ID"

flask db migrate

flask db upgrade