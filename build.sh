#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source ${PWD}/.env
make install && psql -a -d $DATABASE_URL -f database.sql
