FROM python:3.9-slim

WORKDIR /app

COPY producer.py .

RUN pip install confluent-kafka

CMD ["python", "producer.py"]
