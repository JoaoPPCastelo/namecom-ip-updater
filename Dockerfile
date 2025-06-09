FROM python:3.11-slim

RUN pip install requests

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY update_ip.py .

ENTRYPOINT ["python3", "update_ip.py"]
