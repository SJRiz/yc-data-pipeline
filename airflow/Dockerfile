FROM apache/airflow:3.0.3
USER airflow

ENV PYTHONPATH="/opt/airflow/db:${PYTHONPATH}"
# Copy the db folder into the container
COPY ../db /opt/airflow/db

RUN pip install --no-cache-dir bs4 pandas sqlalchemy 'apache-airflow[google]'