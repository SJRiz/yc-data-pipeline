#!/usr/bin/env bash

echo "Creating Airflow connection for external Postgres..."

# Use environment variables, with fallback defaults if not set
PG_USER="${POSTGRES_USER:-postgres}"
PG_PASSWORD="${POSTGRES_PASSWORD:-postgres}"
PG_HOST="${POSTGRES_HOST:-db}"
PG_PORT="${POSTGRES_PORT:-5432}"
PG_DB="${POSTGRES_DB:-postgres}"
CONN_ID="${AIRFLOW_CONN_ID:-postgres_docker}"

# Construct the connection URI
CONN_URI="postgresql+psycopg2://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:${PG_PORT}/${PG_DB}"

# Create the Airflow connection
airflow connections add "$CONN_ID" --conn-uri "$CONN_URI" || \
  echo "Connection already exists or failed"