FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libpq-dev \
    python3-dev \
    build-essential \
    tzdata \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD [ "python3","manage.py","runserver","0.0.0.0:8000" ]
