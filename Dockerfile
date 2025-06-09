FROM python:3.11-slim

RUN pip install requests

WORKDIR /app

COPY update_ip.py .

CMD ["python", "update_ip.py"]
