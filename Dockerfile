FROM python:3.9-slim

ENV IN_DOCKER_CONTAINER=True

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api

EXPOSE 8000

WORKDIR /code/api

CMD ["uvicorn", "main:app"]