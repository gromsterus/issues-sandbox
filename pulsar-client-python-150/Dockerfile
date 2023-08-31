FROM python:3.6-slim

ENV PROJECT_ROOT=/app

WORKDIR $PROJECT_ROOT/
COPY requirements.txt $PROJECT_ROOT/

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

COPY case/ $PROJECT_ROOT/case/
COPY task.py $PROJECT_ROOT/
