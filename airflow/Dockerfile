FROM apache/airflow:3.0.3
USER airflow

WORKDIR /opt/airflow

# Copy lib folder from project root into /opt/airflow/lib inside container
COPY ../libs /opt/airflow/libs

ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"

RUN pip install --no-cache-dir bs4 pandas sqlalchemy dotenv 'apache-airflow[google]'