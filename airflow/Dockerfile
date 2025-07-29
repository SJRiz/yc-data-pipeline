FROM apache/airflow:3.0.3
USER airflow

WORKDIR /opt/airflow

# Copy lib folder from project root into /opt/airflow/lib inside container
COPY ../libs /opt/airflow/libs

ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"

RUN pip install --no-cache-dir bs4 pandas "SQLAlchemy>=1.4,<1.5" dotenv psycopg2-binary 'apache-airflow[google]'