# base image
FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get -y install netcat \
    && apt-get clean


# WORKDIR /app
WORKDIR /code


# COPY Pipfile Pipfile.lock /app/
COPY Pipfile .
COPY Pipfile.lock .


RUN pip install pipenv

RUN pipenv install --system --dev

# COPY . /app/
COPY . .

EXPOSE 8000

CMD ["python", "acme_relutech/manage.py", "runserver", "0.0.0.0:8000"]
