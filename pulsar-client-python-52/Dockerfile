FROM python:3.9

ENV PROJECT_ROOT=/app

WORKDIR $PROJECT_ROOT/
COPY requirements.txt $PROJECT_ROOT/

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

COPY case.py case_fixed.py $PROJECT_ROOT/
