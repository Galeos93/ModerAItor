FROM python:3.10

WORKDIR /app

RUN mkdir moderaitor

COPY requirements.txt .
COPY docker/entrypoint.sh .
COPY moderaitor moderaitor

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "entrypoint.sh"]
