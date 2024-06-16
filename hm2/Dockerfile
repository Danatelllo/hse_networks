FROM python:3.10-slim

WORKDIR /app

COPY mtu.py .

RUN apt-get update && \
    apt-get install -y iputils-ping && \
    rm -rf /var/lib/apt/lists/*

RUN pip install validators

CMD ["python", "mtu.py", "google.com"]
