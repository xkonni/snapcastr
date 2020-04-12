FROM python:3.7-alpine

COPY . /app/

WORKDIR /app/

RUN pip install -e .

EXPOSE 5011

CMD snapcastrd --bind 0.0.0.0 --port=5011 --host "$SNAPCAST_HOST"
