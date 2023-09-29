FROM python:3.11

ENV PROJECT_ROOT=/app

WORKDIR $PROJECT_ROOT/
COPY requirements.txt $PROJECT_ROOT/

RUN pip install --no-cache-dir -r requirements.txt

COPY case.py case_fixed_ext.py case_gunicorn.py gunicorn_conf.py $PROJECT_ROOT/
