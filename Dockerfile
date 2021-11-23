FROM python:3.9-alpine3.12

COPY requirements.txt /var/www/app/requirements.txt

RUN apk update && \
    apk add build-base postgresql-dev python3-dev libffi-dev zlib-dev jpeg-dev git && \
    pip3 install --no-cache-dir --upgrade pip
RUN pip3 install -r /var/www/app/requirements.txt --no-cache-dir && \
    apk del --purge build-base


ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app
ADD . /app

ENTRYPOINT ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "5000", "--log-config", "logging.conf"]
