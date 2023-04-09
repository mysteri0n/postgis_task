#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER $DB_USER;
	CREATE DATABASE $DB_NAME;
	GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
	ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
	\c $DB_NAME;
	CREATE EXTENSION postgis;
EOSQL

ogr2ogr -f "PostgreSQL" PG:"dbname=$DB_NAME user=$POSTGRES_USER password=$POSTGRES_PASSWORD" "/tmp/data/fr-subset.geojsons" -nln fields

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	\c $DB_NAME;
	GRANT USAGE ON SCHEMA public TO $DB_USER;
	GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
EOSQL