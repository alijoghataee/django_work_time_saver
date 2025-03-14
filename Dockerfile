FROM python:3.12
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD python manage.py migrate &&gunicorn --reload --bind 0.0.0.0:8000 --access-logfile - core.wsgi:application