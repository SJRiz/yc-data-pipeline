FROM python:3.11.9-slim

WORKDIR /streamlit

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard/ ./dashboard/
COPY ../libs/ ./dashboard/libs/

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
