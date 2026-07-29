FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY enterprise/api-service/app/ app/
COPY enterprise/api-service/tests/ tests/

CMD ["python", "app/main.py"]
