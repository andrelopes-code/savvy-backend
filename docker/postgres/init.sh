#!/bin/bash


set -e  # exit asap if a command exits with a non-zero status
set -u  # treat unset variables as an error and exit

function create_user_and_database() {
	local database=$1
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	    CREATE USER $database PASSWORD '$DATABASE_PASSWORD';
	    CREATE DATABASE $database;
	    GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL
}

if [ -n "$POSTGRES_DBS" ]; then
	echo "Creating DB(s): $POSTGRES_DBS"
	for db in $(echo $POSTGRES_DBS | tr ',' ' '); do
		create_user_and_database $db
	done
	echo "Multiple databases created"
fi