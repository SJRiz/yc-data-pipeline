FROM apache/airflow:3.0.3

# Use the airflow user
USER airflow

# Set working directory inside the container
WORKDIR /opt/airflow

# Copy  libs
COPY ../libs /opt/airflow/libs

# Set the PYTHONPATH so Airflow and Python can find your custom modules
ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"

# Copy the connection creation script
COPY airflow/scripts/create_connections.sh /opt/airflow/scripts/create_connections.sh

USER root
RUN chmod +x /opt/airflow/scripts/create_connections.sh
USER airflow

# Install required Python packages
RUN pip install --no-cache-dir \
    bs4 \
    pandas \
    "SQLAlchemy>=1.4,<1.5" \
    python-dotenv \
    psycopg2-binary \
    'apache-airflow[google]'
