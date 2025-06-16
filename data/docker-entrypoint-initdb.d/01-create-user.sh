#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    -- Create cms_user user
    CREATE USER cms_user WITH PASSWORD '${POSTGRES_CMS_USER_PASSWORD}';
EOSQL
