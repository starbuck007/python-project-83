#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source .env
make install && psql -a -d $DATABASE_URL -f database.sql
