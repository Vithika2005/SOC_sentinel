FROM python:3.8-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY tests/ tests/

CMD ["python", "app/main.py"]
