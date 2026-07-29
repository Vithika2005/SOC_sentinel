FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY enterprise/legacy-admin/app/ app/
COPY enterprise/legacy-admin/templates/ templates/

CMD ["python", "app/main.py"]
