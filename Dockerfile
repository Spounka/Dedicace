FROM python:3.10.7-bullseye

ENV PYTHONUNBERFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code/
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /code
