FROM python:3.9-slim

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api

EXPOSE 8000

WORKDIR /code/api

CMD ["python3", "main.py"]