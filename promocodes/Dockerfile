FROM python:3.12.8-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/app'

WORKDIR /opt/app
COPY requirements.txt /opt/app/requirements.txt
RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r /opt/app/requirements.txt

COPY app/ /opt/app

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
