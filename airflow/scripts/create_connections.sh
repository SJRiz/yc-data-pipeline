#!/usr/bin/env bash

echo "Creating Airflow connection for external Postgres..."

airflow connections add 'postgres_docker' \
  --conn-uri 'postgresql+psycopg2://postgres:Water123@db:5432/postgres' || \
  echo "Connection already exists or failed"

