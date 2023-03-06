FROM python:3
WORKDIR /code

COPY . /code/
RUN pip install -r webstore/requirements.txt
