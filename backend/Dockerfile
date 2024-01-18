FROM python:3.9-slim

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x entrypoint.sh entrypoint_daphne.sh

ENTRYPOINT ["/app/entrypoint.sh"]