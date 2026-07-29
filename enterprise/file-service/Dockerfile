FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY enterprise/file-service/app/ app/

CMD ["python", "app/main.py"]
