FROM python:3.10-slim

WORKDIR /app

COPY mtu.py .

RUN pip install validators

CMD ["python", "mtu.py", "google.com"]
